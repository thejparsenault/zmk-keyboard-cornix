# Cornix Vial keymap

Source: `/Users/jp/Downloads/cornix.vil`.

| ZMK layer | Vial layer | Access |
| --- | --- | --- |
| 0 Base | 0 | Default |
| 1 Navigation | 1 | Hold the left Backspace thumb key |
| 2 Numpad | 2 | Hold the right Space thumb key |
| 3 Symbols | 5 | Hold either symbols key (originally MO(5)) |

Unused Vial layers are omitted. The original Delete layer-tap is plain Delete.
All 50 physical positions are mapped, including both encoder clicks. The Vial
right-hand matrix is reversed into ZMK physical left-to-right order. Disabled
keys remain disabled rather than becoming transparent. Inherited combos and conditional layers are omitted because they are not in
the Vial export. Positional home-row behaviors are retained by user preference.

Bluetooth mappings, confirmed by the user: USER00/01/02 select host 1/2/3
(ZMK profiles 0/1/2); USER05 clears the selected host pairing. No additional
output-switch or split-peer-reset bindings are added.

Encoder intent: left counterclockwise scrolls up, clockwise scrolls down;
right counterclockwise lowers volume, clockwise raises it. Scrolling uses
100 wheel units/second with a 10 ms reporting period and no acceleration,
so a 20 ms encoder pulse produces whole wheel units instead of discarded
fractions. These actions are
repeated on every active layer to reproduce Vial transparent encoder bindings.
Confirm direction on the physical hardware; the two firmware implementations
may interpret encoder wiring differently. Left click is play/pause, right click
is mute, and higher layers inherit those clicks.

Home-row modifier keys use the shipped Cornix custom behaviors: `hm_l` and
`hm_r` use balanced flavor with a 250 ms tapping term; `hm_shift_r` uses
200 ms for Quote/Right Shift. All use a 200 ms quick-tap window, 70 ms
prior-idle requirement, opposite-hand plus selected thumb trigger positions,
and hold-trigger-on-release. Escape/Right Alt also uses `hm_l`. Dedicated
Shift and modifier keys remain ordinary key presses.

Space and Backspace retain tap-preferred layer-taps at 250 ms, with quick-tap
repeat disabled. Test rolling letters, shortcuts, Quote/Shift, and thumb layer
access on hardware; this is not a claim of identical Vial timing.

## Build configuration

`config/cornix.keymap` is the active keymap. `config/cornix.conf` explicitly
enables `CONFIG_ZMK_POINTING=y` for mouse-wheel emulation. Encoder drivers
are already enabled in the board defaults. Both direct-left-central and dongle
build targets remain available in `build.yaml`.

Keycode names and 50 bindings per layer were checked locally. Hardware typing
feel and encoder direction still need testing after flashing.

## Status indicators and Studio

The indicator module is vendored under `modules/zmk-rgbled-widget`; upstream
revision and local policy are recorded in `UPSTREAM.md`. Normal idle wake
stays dark, with a 5-second grace period before showing an unresolved connection.
Boot, Bluetooth profile changes, and active connection changes retain upstream
animations. Low battery reminders are limited to every five minutes; critical
battery escalates immediately. Charging detection remains based on USB power.
Caps Lock and layer indications are disabled. A reboot retains startup lights.

The direct left-central build includes `studio-rpc-usb-uart`; connect that half
by USB to use Studio. Studio was already enabled in the board defaults.
