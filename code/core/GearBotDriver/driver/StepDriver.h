#ifndef StepDriver_h
#define StepDriver_h

#include <Arduino.h>
#include <stdlib.h>

#define STEP_PER_REVOLUTION 200.0
#define START_STOP_EXPONENT 4
#define FULL_CIRCLE 360.0

#define degrees_to_steps(angle) angle / (360.0f / (_step * STEP_PER_REVOLUTION));
#define steps_to_degrees(steps) 360.0f / (_step * STEP_PER_REVOLUTION) * steps;

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
    StepDriver(Stepsize, int, int, float);

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
    long get_position() { return _current_position; };
    long get_target() { return _target_position; };
    float degrees_to_target() { return steps_to_degrees(abs(_current_position - _target_position)) };
    long steps_to_target() { return abs(_current_position - _target_position); };

    void set_speed(int);
    void set_angle(float);

    void set_gearbox_ratio(int ratio) { _gearbox_ratio = ratio; };

    void set_accel_steps(int steps) { _accel_steps = steps; };
    void set_accel_deg(int degrees) { _accel_steps = degrees_to_steps(degrees); };

    void set_decel_steps(int steps) { _decel_steps = steps; };
    void set_decel_deg(int degrees) { _decel_steps = degrees_to_steps(degrees); };

    void accel_percent(int percent) { _accel_percent = percent; };
    void decel_percent(int percent) { _decel_percent = percent; };

    void set_ramp_multiplier(float scale) { _slow_ramp_multiplier = scale; };
    
  private:
    int _accel_percent;
    int _decel_percent;

    int _accel_steps;
    int _curr_accel_steps;
    
    int _decel_steps;
    int _curr_decel_steps;
    
    int _dir_pin;
    int _step_pin;
    long _target_position;
    long _current_position;
    
    float _angle;
    float _gearbox_ratio;
    float _slow_ramp_multiplier;

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