#version 330

in vec3 vertexPosition;
in vec3 vertexNormal;
in vec3 vertexColor;  // Color of the object

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 fragNormal;
out vec3 fragPosition;
out vec3 fragColor;  // Pass the object color to the fragment shader

void main() {
    fragPosition = vec3(model * vec4(vertexPosition, 1.0));
    fragNormal = mat3(transpose(inverse(model))) * vertexNormal;
    fragColor = vertexColor;  // Pass the object color

    gl_Position = projection * view * vec4(fragPosition, 1.0);
}