"""Hardware-independent note handling, touch filtering and MIDI CC mapping."""


def clamp(value, low=0, high=127):
    return max(low, min(high, value))


class TouchFilter:
    def __init__(self, baselines, press_ratio, release_ratio, debounce):
        if not 1 < release_ratio < press_ratio:
            raise ValueError("Touch ratios must satisfy 1 < release < press")
        if not baselines or any(v <= 0 for v in baselines):
            raise ValueError("Touch baselines must be positive")
        self.press = [v * press_ratio for v in baselines]
        self.release = [v * release_ratio for v in baselines]
        self.states = [False] * len(baselines)
        self.candidates = [False] * len(baselines)
        self.changed = [0.0] * len(baselines)
        self.debounce = debounce

    def update(self, values, now):
        if len(values) != len(self.states):
            raise ValueError("Touch sample count changed")
        events = []
        for i, value in enumerate(values):
            threshold = self.release[i] if self.states[i] else self.press[i]
            detected = value > threshold
            if detected != self.candidates[i]:
                self.candidates[i] = detected
                self.changed[i] = now
            if (detected != self.states[i]
                    and now - self.changed[i] >= self.debounce):
                self.states[i] = detected
                events.append((i, detected))
        return events


class Controller:
    def __init__(self, cfg, send):
        self.cfg = cfg
        self.send = send
        if len(cfg.MELODY_NOTES) != len(cfg.DRUM_NOTES):
            raise ValueError("Note maps must have equal lengths")
        for channel in (cfg.MELODY_CHANNEL, cfg.DRUM_CHANNEL):
            if not 0 <= channel <= 15:
                raise ValueError("MIDI channels must be 0..15")
        for note in cfg.MELODY_NOTES:
            if not (0 <= note + 12 * cfg.MIN_OCTAVE_SHIFT
                    <= note + 12 * cfg.MAX_OCTAVE_SHIFT <= 127):
                raise ValueError("Octave range exceeds MIDI note limits")
        if any(not 0 <= note <= 127 for note in cfg.DRUM_NOTES):
            raise ValueError("Drum notes must be 0..127")
        if not 1 <= cfg.NOTE_VELOCITY <= 127:
            raise ValueError("Velocity must be 1..127")
        if cfg.SLIDER_ADC_MAX <= cfg.SLIDER_ADC_MIN:
            raise ValueError("Slider ADC range must be positive")
        if not 0 < cfg.SLIDER_FILTER_ALPHA <= 1:
            raise ValueError("Slider filter alpha must be 0..1")
        self.mode = "melody"
        self.octave_shift = 0
        self.held = [False] * len(cfg.MELODY_NOTES)
        self.active = [None] * len(self.held)
        self.encoder_value = cfg.ENCODER_INITIAL_VALUE
        self.slider_value = None
        self.slider_filtered = None
        self.last_slider_sent = None

    @property
    def channel(self):
        return (self.cfg.MELODY_CHANNEL if self.mode == "melody"
                else self.cfg.DRUM_CHANNEL)

    def cc(self, controller, value):
        self.send(bytes((0xB0 | self.channel, controller, clamp(int(value)))))

    def pad(self, index, down):
        if self.held[index] == down:
            return
        self.held[index] = down
        if down:
            note = (self.cfg.MELODY_NOTES[index] + 12 * self.octave_shift
                    if self.mode == "melody" else self.cfg.DRUM_NOTES[index])
            self.send(bytes((0x90 | self.channel, note, self.cfg.NOTE_VELOCITY)))
            self.active[index] = (note, self.channel)
        elif self.active[index] is not None:
            note, channel = self.active[index]
            self.send(bytes((0x80 | channel, note, 0)))
            self.active[index] = None

    def panic(self):
        for i, active in enumerate(self.active):
            if active is not None:
                note, channel = active
                self.send(bytes((0x80 | channel, note, 0)))
                self.active[i] = None
        for channel in (self.cfg.MELODY_CHANNEL, self.cfg.DRUM_CHANNEL):
            self.send(bytes((0xB0 | channel, 123, 0)))
        # Keep held states: release/re-touch is required after a panic.

    def sync_controls(self):
        self.cc(self.cfg.ENCODER_CC, self.encoder_value)
        if self.slider_value is not None:
            self.cc(self.cfg.SLIDER_CC, self.slider_value)
            self.last_slider_sent = self.slider_value

    def button(self, name):
        if name == "mode":
            self.panic()
            self.mode = "drums" if self.mode == "melody" else "melody"
            self.sync_controls()
        elif name in ("octave_down", "octave_up") and self.mode == "melody":
            step = -1 if name == "octave_down" else 1
            value = clamp(self.octave_shift + step,
                          self.cfg.MIN_OCTAVE_SHIFT, self.cfg.MAX_OCTAVE_SHIFT)
            if value != self.octave_shift:
                self.panic()
                self.octave_shift = value
        elif name == "function":
            self.panic()
        elif name == "encoder":
            self.encoder_value = self.cfg.ENCODER_INITIAL_VALUE
            self.cc(self.cfg.ENCODER_CC, self.encoder_value)

    def encoder(self, delta):
        value = clamp(self.encoder_value + int(delta))
        if value != self.encoder_value:
            self.encoder_value = value
            self.cc(self.cfg.ENCODER_CC, value)

    def slider(self, raw):
        cfg = self.cfg
        raw = clamp(raw, cfg.SLIDER_ADC_MIN, cfg.SLIDER_ADC_MAX)
        if self.slider_filtered is None:
            self.slider_filtered = raw
        else:
            self.slider_filtered += cfg.SLIDER_FILTER_ALPHA * (raw - self.slider_filtered)
        normalized = ((self.slider_filtered - cfg.SLIDER_ADC_MIN)
                      / (cfg.SLIDER_ADC_MAX - cfg.SLIDER_ADC_MIN))
        if cfg.SLIDER_INVERT:
            normalized = 1 - normalized
        self.slider_value = clamp(int(normalized * 127 + 0.5))
        previous = self.last_slider_sent
        if (previous is None or abs(self.slider_value - previous) >= cfg.SLIDER_CC_STEP
                or (self.slider_value in (0, 127) and self.slider_value != previous)):
            self.cc(cfg.SLIDER_CC, self.slider_value)
            self.last_slider_sent = self.slider_value

    def colors(self):
        idle = (20, 60, 180) if self.mode == "melody" else (180, 40, 5)
        return [(255, 255, 255) if note is not None else idle
                for note in self.active]
