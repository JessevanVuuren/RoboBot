            # origin = vector3_to_matrix(part.link.start_pos)
            # final_position = matrix_multiply(part_offset, origin)

            part_offset = part.offset

            # 2. Apply the first local rotation (around X)
            angle = math.atan2(self.link1.end_pos.y, self.link1.end_pos.z)
            woow = matrix_rotate_x(-angle)
            print(angle)
            # 3. Apply the yaw rotation (around Y) 
            yaw_rotation = matrix_rotate_y(self.yaw)

            # 4. Multiply the matrices in the correct order:
            # Final transformation = Translate -> RotateX -> RotateY
            anchor_point = matrix_multiply(part_offset, matrix_multiply(woow, yaw_rotation))


            # 5. Set the final position
            part.position = anchor_point