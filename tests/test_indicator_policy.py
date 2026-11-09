"""Host-side checks of the actual indicator callback bodies (no Zephyr SDK needed)."""
from pathlib import Path
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'modules/zmk-rgbled-widget/src/widget.c'


def function(source, name):
    # Skip forward declarations when locating the implementation.
    import re
    match = re.search(r'static (?:int|void) ' + name + r'\([^;]*?\) \{', source)
    start = match.start()
    opening = source.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


class IndicatorPolicy(unittest.TestCase):
    def test_connection_events(self):
        source = SOURCE.read_text()
        callbacks = '\n'.join(function(source, name) for name in (
            'led_output_listener_cb', 'wake_check_cb', 'indicate_connectivity_cb'))
        harness = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#define ZMK_ACTIVITY_ACTIVE 0
#define ZMK_ACTIVITY_IDLE 1
struct k_work { int unused; };
struct k_work_delayable { int unused; };
typedef int zmk_event_t;
static bool initialized = true, quiet_wake, connected;
static int current_activity_state, last_profile, profile, indications;
static int64_t wake_deadline, now;
static struct k_work_delayable wake_check_work;
static int indicator_profile(void) { return profile; }
static int64_t k_uptime_get(void) { return now; }
static void k_work_cancel_delayable(struct k_work_delayable *w) { (void)w; }
static bool indicator_connection_ready(void) { return connected; }
static void indicate_connectivity(void) { indications++; }
static void indicate_connectivity_internal(void) { indications++; }
'''
        scenarios = r'''
int main(void) {
    // Successful wake reconnect is silent, including its queued callback.
    quiet_wake = true; wake_deadline = 5000; now = 1000;
    connected = true;
    led_output_listener_cb(NULL); indicate_connectivity_cb(NULL);
    assert(indications == 0);
    now = 5000; wake_check_cb(NULL);
    assert(!quiet_wake && indications == 0);
    // Active connection loss is not hidden after successful wake.
    connected = false; led_output_listener_cb(NULL);
    assert(indications == 1);
    // An unresolved wake reconnect shows the normal indication at timeout.
    quiet_wake = true; wake_deadline = 10000; now = 10000;
    wake_check_cb(NULL); assert(indications == 2 && !quiet_wake);
    // Intentional profile switch bypasses the wake grace.
    quiet_wake = true; wake_deadline = 20000; now = 11000; profile = 1;
    led_output_listener_cb(NULL); assert(indications == 3 && !quiet_wake);
    // Idle connection events and stale animation callbacks remain dark.
    current_activity_state = ZMK_ACTIVITY_IDLE; quiet_wake = true;
    led_output_listener_cb(NULL); wake_check_cb(NULL); indicate_connectivity_cb(NULL);
    assert(indications == 3);
    // Boot/active callbacks still display normal animations.
    current_activity_state = ZMK_ACTIVITY_ACTIVE; quiet_wake = false;
    indicate_connectivity_cb(NULL); assert(indications == 4);
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as directory:
            cfile = Path(directory) / 'policy.c'
            exe = Path(directory) / 'policy'
            cfile.write_text(harness + callbacks + scenarios)
            subprocess.run(['cc', '-std=c99', '-Wall', '-Werror', str(cfile), '-o', str(exe)], check=True)
            subprocess.run([str(exe)], check=True)


if __name__ == '__main__':
    unittest.main()
