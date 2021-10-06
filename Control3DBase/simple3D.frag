varying vec4 v_normal;
varying vec4 v_position;

varying vec2 v_uv;
uniform sampler2D u_tex_diffuse;
uniform vec4 u_eye_position;

uniform vec4 u_global_light_direction;
uniform vec4 u_global_light_color;

uniform vec4 u_mat_diffuse;
uniform float u_mat_shiny;
uniform float u_mat_emit;

vec4 calculate_directional_light()
{
	/*
	Since this is a directional light, we don't need to calculate its' direction.
    For some weird reason, the "standard" thing to do is
    to face the light away from the scene,
    and then reverse it in the shader.
	*/
	vec4 light_dir = normalize(-u_global_light_direction);
    // Get the vector from the camera to the fragment
	vec4 v = normalize(u_eye_position - v_position);
    /*
	Get the halfway vector between the light direction
	and the eye direction.
    It's used to calculate the specularity.
	*/
	vec4 vh = normalize(light_dir + v);

    // Calculate the true color of the material.
	float lambert = max(dot(v_normal, light_dir), 0.0);
    // Calculate the specularity/shininess.
	float phong = max(dot(v_normal, vh), 0.0);

    // Combine the values, along with a little bit of ambience.
	return u_global_light_color * u_mat_diffuse * lambert
			+ u_global_light_color * pow(phong, u_mat_shiny)
			+ (u_global_light_color * 0.01);
}

void main(void)
{
    gl_FragColor = texture2D(u_tex_diffuse, v_uv);
    //glFragColor = v_color;
}