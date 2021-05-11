#version 430

in vec3 a_position;
in vec3 a_color;

uniform mat4 viewMat;
uniform mat4 projMat;

out vec3 v_color;

void main()
{
    gl_Position = projMat * viewMat * vec4(a_position, 1.0);
    v_color = a_color;
}