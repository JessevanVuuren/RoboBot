#version 330

in vec3 fragNormal;
in vec3 fragPosition;
in vec3 fragColor;  // Object color passed from vertex shader

uniform vec3 lightPosition;
uniform vec3 lightColor;

void main() {
    // Normalize normal and light direction
    vec3 normal = normalize(fragNormal);


    vec3 lightDir = normalize(lightPosition - fragPosition);

    // Diffuse lighting calculation
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Calculate final color
    vec3 diffuse = diff * lightColor * fragColor;
    vec3 ambient = 0.2 * fragColor;  // Simple ambient lighting
    
    gl_FragColor = vec4(diffuse + ambient, 1.0);
}
