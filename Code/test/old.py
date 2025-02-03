    # if (is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT)):
    #     mouseDelta = get_mouse_delta()
    #     camera_yaw(camera, -mouseDelta.x * .01, True)
    #     camera_pitch(camera, -mouseDelta.y * .01, True, True, False)    

    # end_effector_xz = Vector2(point_to_follow.x, point_to_follow.z)
    # origin_point_xz = Vector2(origin_point.x, origin_point.z)

    # xz_distance = vector2_distance(end_effector_xz, origin_point_xz)
    # vertical_offset = point_to_follow.y - link1.start_pos.y
    # base_angle = math.atan2(vertical_offset, xz_distance)

    # distance = math.sqrt(xz_distance**2 + vertical_offset**2)
    # distance = min(distance, arm_reach)

    # alpha = math.acos((distance**2 + arm_length**2 - arm_length**2) / (2 * distance * arm_length))
    # beta = math.acos((arm_length**2 + arm_length**2 - distance**2) / (2 * arm_length * arm_length))

    # yaw = math.atan2(point_to_follow.x, point_to_follow.z)

    # angle1 = base_angle + alpha
    # angle2 = math.pi - beta

    # link1.set_angle_x(angle1)
    # link1.set_angle_y(-yaw)

    # link2.set_start_point(link1.end_pos)
    # link2.set_angle_x(angle1 - angle2)
    # link2.set_angle_y(-yaw)




    # angle = math.atan2(camera.position.x, camera.position.z) # y
    # angle = math.atan2(camera.position.y, camera.position.x) # z
    # angle = math.atan2(camera.position.z, camera.position.y) # x
    
    # matrix = matrix_rotate(xyz.y.control_axis, angle)

    # ma = matrix_multiply(xyz.y.hidden_plane_matrix, matrix)
    # ma = matrix_multiply(ma, vector3_to_matrix(target))

    # draw_mesh(xyz.hidden_plane, xyz.x.hit_box.material, ma)