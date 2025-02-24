#ifndef StepDriver_h
#define StepDriver_h

#include <Arduino.h>
#include <stdlib.h>

#define STEP_PER_REVOLUTION 200.0
#define START_STOP_EXPONENT 4

#define degrees_to_steps(angle, step) angle / (360.0f / (_step * STEP_PER_REVOLUTION));

typedef enum {
    FULL_STEP = 1,
    HALF_STEP = 2,
    FOUR_STEP = 4,
    EIGHT_STEP = 8,
    SIXTEEN_STEP = 16,
    THIRTYTHREE_STEP = 32,
} Stepsize;

class StepDriver {


  public:
    StepDriver(Stepsize step, int dir_pin, int step_pin);

    void run();
    void run_absolute();
    void run_blocked();
    
    void display_info();

    void next_step(int);
    void absolute_step(int);

    void next_angle(float);
    void absolute_angle(float);

    // True -> clockwise, false -> counter clockwise
    void set_direction(bool);

    float get_interval() { return _step_interval; };
    float get_angle() { return _angle; };
    int get_position() { return _current_position; };
    int get_target() { return _target_position; };
    int steps_to_target() { return abs(_current_position - _target_position); };

    void set_speed(int);

    void set_accel_steps(int steps) { _accel_steps = steps; };
    void set_accel_deg(int degrees) { _accel_steps = degrees_to_steps(degrees, _step); };

    void set_decel_steps(int steps) { _decel_steps = steps; };
    void set_decel_deg(int degrees) { _decel_steps = degrees_to_steps(degrees, _step); };

    void set_ramp_multiplier(int scale) { _slow_ramp_multiplier = scale; };

    void accel_percent(int percent) { _accel_percent = percent; };
    void decel_percent(int percent) { _decel_percent = percent; };

  private:
    int _accel_percent;
    int _decel_percent;

    int _accel_steps;
    int _curr_accel_steps;

    int _decel_steps;
    int _curr_decel_steps;

    int _dir_pin;
    int _step_pin;
    int _target_position;
    int _current_position;

    int _slow_ramp_multiplier;

    float _angle;

    unsigned long _last_step_time;
    unsigned long _step_interval;

    bool _direction;
    Stepsize _step;

    long _calculate_ramp(int, int *, int, bool);
    void _step_motor();
    void _target_reached();
    void _recalculate_ramp(int);
};

#endif