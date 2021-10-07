varying vec4 v_normal;
varying vec4 v_position;

varying vec2 v_uv;
uniform sampler2D u_tex_diffuse;
uniform sampler2D u_tex_specular;

uniform vec4 u_eye_position;

uniform vec4 u_global_light_direction;
uniform vec4 u_global_light_color;

uniform vec4 u_global_flashlight_direction;
uniform vec4 u_global_flashlight_color;
uniform float use_flashlight;


uniform float u_mat_shiny;
uniform float u_mat_emit;



vec4 calculate_directional_light()
{
	vec4 light_dir = normalize(-u_global_light_direction);
	vec4 v = normalize(u_eye_position - v_position);
	vec4 vh = normalize(light_dir + v);
	float lambert = max(dot(v_normal, light_dir), 0.0);
	float phong = max(dot(v_normal, vh), 0.0);
	return u_global_light_color * texture2D(u_tex_diffuse, v_uv) * lambert
			+ u_global_light_color * texture2D(u_tex_specular, v_uv) * pow(phong, u_mat_shiny)
			+ (u_global_light_color * 0.01);
}
vec4 calculate_flashlight()
{
	vec4 flashlight_dir = normalize(u_global_flashlight_direction);
	vec4 f = normalize(u_eye_position - v_position);
	vec4 fvh = normalize(flashlight_dir + f);
	float lambert = max(dot(v_normal, flashlight_dir), 0.0);
	float phong = max(dot(v_normal, fvh), 0.0);
	return u_global_flashlight_color * texture2D(u_tex_diffuse, v_uv) * lambert
			+ u_global_flashlight_color * texture2D(u_tex_specular, v_uv) * pow(phong, u_mat_shiny)
			+ (u_global_flashlight_color * 0.01);

}
void main(void)
{
	if(use_flashlight>=0.0){
		gl_FragColor = calculate_directional_light();
		gl_FragColor += calculate_flashlight();
	}
		if(use_flashlight==0.0){
		gl_FragColor = calculate_directional_light();
	}

    //gl_FragColor = texture2D(u_tex_diffuse, v_uv);
    //glFragColor = v_color;
}