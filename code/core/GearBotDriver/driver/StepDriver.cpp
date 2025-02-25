#include "StepDriver.h"

StepDriver::StepDriver(Stepsize step, int dir_pin, int step_pin, float gearbox_ratio) {
    pinMode(dir_pin, OUTPUT);
    pinMode(step_pin, OUTPUT);

    _direction = true;
    set_direction(true);

    _step_pin = step_pin;
    _dir_pin = dir_pin;
    _step = step;

    _slow_ramp_multiplier = 2;

    _curr_accel_steps = 0;
    _curr_decel_steps = 0;
    _accel_percent = 0;
    _decel_percent = 0;
    _accel_steps = 0;
    _decel_steps = 0;

    _current_position = 0;
    _target_position = 0;

    _last_step_time = 0;
    _step_interval = 0;

    _gearbox_ratio = gearbox_ratio;
    _angle = 0;
}

void StepDriver::set_speed(int rpm) {
    float steps_per_sec = (_step * STEP_PER_REVOLUTION * rpm) / 60.0;
    float second_per_step = (1 / steps_per_sec);

    _step_interval = second_per_step * 1000000;
}

void StepDriver::set_angle(float degrees) {
    _angle = degrees;
}

void StepDriver::run() {
    if (_current_position != _target_position) {
        set_direction(_current_position < _target_position);
        _step_motor();

        if (_current_position == _target_position) {
            _target_reached();
        }
    }
}

void StepDriver::run_absolute() {
    _step_motor();
}

void StepDriver::_step_motor() {
    unsigned long time = micros();

    if (time > _last_step_time) {
        digitalWrite(_step_pin, HIGH);
        delayMicroseconds(1);
        digitalWrite(_step_pin, LOW);

        long sleep = _step_interval;
        int diff = abs(_target_position - _current_position);
        if (_accel_steps < diff) sleep = _calculate_ramp(_step_interval, &_curr_accel_steps, _accel_steps, true);
        if (_decel_steps > diff) sleep = _calculate_ramp(_step_interval, &_curr_decel_steps, _decel_steps, false);
        
        _last_step_time = time + sleep;

        _current_position += _direction ? 1 : -1;
    }
}

void StepDriver::_target_reached() {
    _curr_accel_steps = 0;
    _curr_decel_steps = 0;
}

void StepDriver::run_blocked() {
    long sleep = _calculate_ramp(_step_interval / 2, &_curr_accel_steps, _accel_steps, true);

    digitalWrite(_step_pin, HIGH);
    delayMicroseconds(sleep);
    digitalWrite(_step_pin, LOW);
    delayMicroseconds(sleep);
}

void StepDriver::next_angle(float degrees) {
    float steps = degrees_to_steps(degrees);
    
    steps *= _gearbox_ratio;
    _recalculate_ramp(steps);

    _target_position += steps;
    _angle += degrees;
}

void StepDriver::absolute_angle(float degrees) {
    float delta = degrees - _angle;

    if (delta > 0 && _angle > degrees) delta -= FULL_CIRCLE;
    if (delta < 0 && degrees > _angle) delta += FULL_CIRCLE;

    next_angle(delta);
}

void StepDriver::next_step(int steps) {
    steps *= _gearbox_ratio;
    _recalculate_ramp(steps);
    _target_position += steps;
}

void StepDriver::absolute_step(int steps) {
    steps *= _gearbox_ratio;
    _recalculate_ramp(steps);
    _target_position = steps;
}

long StepDriver::_calculate_ramp(int max_delay, int *current, int total, bool ascending) {
    if (*current >= total) return max_delay;

    (*current)++;

    float exp_current = powf(*current, START_STOP_EXPONENT);
    float exp_steps = powf(total, START_STOP_EXPONENT);

    float progress = ascending ? (1.0f - exp_current / exp_steps) : (exp_current / exp_steps);

    unsigned long extra_delay = max_delay * _slow_ramp_multiplier * progress;
    unsigned long total_delay = max_delay + extra_delay;

    return constrain(total_delay, max_delay, (max_delay * (_slow_ramp_multiplier + 1)));
}

void StepDriver::_recalculate_ramp(int steps) {
    float percent = (abs(steps) / 100.0f);

    if (_accel_percent > 0) _accel_steps = percent * _accel_percent;
    if (_decel_percent > 0) _decel_steps = percent * _decel_percent;
}

void StepDriver::set_direction(bool direction) {
    _direction = direction;
    digitalWrite(_dir_pin, direction);
}


void StepDriver::display_info() {
    Serial.print("pos: ");
    Serial.print(get_position());
    Serial.print(", target:");
    Serial.print(get_target());
    Serial.print(", distance: ");
    Serial.println(steps_to_target());
}
