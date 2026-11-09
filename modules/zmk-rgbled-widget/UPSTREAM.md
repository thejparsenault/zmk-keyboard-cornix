Vendored from https://github.com/hitsmaxft/zmk-rgbled-widget at a2b29334b8598d7351c1f4429c5c083b2c0a3bc5.

Local policy: silent idle wake with a configurable 5-second connection grace;
profile switches and active connection failures retain upstream animations.
Healthy battery is shown at boot, not on every wake. Low battery reminders
are limited to once per 5 minutes, with an immediate escalation to critical.
Charging behavior is retained. Caps Lock and layer indications are disabled
in the Cornix indicator shield configuration.
