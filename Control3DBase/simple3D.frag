varying vec4 v_normal;
varying vec4 v_position;

varying vec2 v_uv;
uniform sampler2D u_tex_diffuse;
uniform sampler2D u_tex_specular;

uniform vec4 u_eye_position;

uniform vec4 u_normal_light_direction;
uniform vec4 u_normal_light_color;

uniform vec4 u_light_position;
uniform vec4 u_light_direction;
uniform vec4 u_light_color;
uniform float u_light_cutoff;
uniform float u_light_outer_cutoff;
uniform float u_light_constant;
uniform float u_light_linear;
uniform float u_light_quad;

uniform vec4 u_flashlight_position;
uniform vec4 u_flashlight_direction;
uniform vec4 u_flashlight_color;
uniform float use_flashlight;
uniform float u_flashlight_cutoff;
uniform float u_flashlight_outer_cutoff;
uniform float u_flashlight_constant;
uniform float u_flashlight_linear;
uniform float u_flashlight_quad;


uniform float u_mat_shiny;
uniform float u_mat_emit;


//Step by step guide on https://learnopengl.com/Lighting/Light-casters
vec4 calculate_directional_light()
{
	/*Directional light is made by defining a light direction vector instead of a position vector,
	we have to negate the global light direction vector to switch its direction,
	and normalize the vector since it is unwise to assume the input vector to be a unit vector.
	*/
	vec4 light_direction = normalize(-u_normal_light_direction);
	vec4 v = normalize(u_eye_position - v_position);
	vec4 vh = normalize(light_direction + v);
	float lambert = max(dot(v_normal, light_direction), 0.0);
	float phong = max(dot(v_normal, vh), 0.0);
	return u_normal_light_color * texture2D(u_tex_diffuse, v_uv) * lambert
			+ u_normal_light_color * texture2D(u_tex_specular, v_uv) * pow(phong, u_mat_shiny)
			+ (u_normal_light_color * 0.01);
	/*
	 Because all of the light rays are parallel,
	 it makes no difference how each object is positioned in relation to the light source
	 because the light direction is the same for all of the objects in the scene.
	 Because the light's direction vector is constant,
	 the lighting computations for each object in the scene will be similar.
	 */
}
vec4 calculate_light()
{
	/* Made the light position to be the same as the players position, but the y values is a bit higher up
	and point the directional vector down to get a small light around the player*/
	vec4 light_dir = normalize(u_light_position - v_position); //the vector pointing from the fragment to the light source.
	//Theta is the angle between the Light_dir vector and the u_light_direction vector.
	//The θ value should be smaller than Φ to be inside the spotlight.
	float theta = dot(light_dir, normalize(u_light_direction));
	float epsilon = u_light_cutoff - u_light_outer_cutoff;
	//calculate the theta θ value and compare this with the cutoff ϕ
	//value to determine if we're in or outside the spotlight:
	float intensity = clamp((theta - u_light_outer_cutoff) / epsilon, 0.0, 1.0);
	vec4 f = normalize(u_eye_position - v_position);
	vec4 fvh = normalize(light_dir + f);
	float lambert = max(dot(v_normal, light_dir), 0.0);
	float phong = max(dot(v_normal, fvh), 0.0);
	float distance    = length(u_light_position - v_position);
	float attenuation = 1.0 / (u_light_constant + u_light_linear * distance + //reduce the intensity of light over the distance
    		    			   u_light_quad * (distance * distance));
	/*
	Then we include this attenuation value in the lighting calculations
	by multiplying the attenuation value with the ambient, diffuse and specular colors.
	*/
	vec4 u_light_color = attenuation *(intensity * u_light_color);
	return u_light_color * texture2D(u_tex_diffuse, v_uv) * lambert
			+ u_light_color * texture2D(u_tex_specular, v_uv) * pow(phong, u_mat_shiny)
			+ (u_light_color * 0.01);

}
vec4 calculate_flashlight()
{
	/*same as with the player lantern light, only difference is that the flashlight position
	is the same as the players position, and the direction of the flashlight is the view_matrix_n*/
	vec4 flashlight_dir = normalize(u_flashlight_position - v_position);
	//Theta is the angle between the Light_dir vector and the u_light_direction vector.
	//The θ value should be smaller than Φ to be inside the spotlight.
	float theta = dot(flashlight_dir, normalize(u_flashlight_direction));
	float epsilon = u_flashlight_cutoff - u_flashlight_outer_cutoff;
	//calculate the theta θ value and compare this with the cutoff ϕ
	//value to determine if we're in or outside the spotlight:
	float intensity = clamp((theta - u_flashlight_outer_cutoff) / epsilon, 0.0, 1.0);
	vec4 f = normalize(u_eye_position - v_position);
	vec4 fvh = normalize(flashlight_dir + f);
	float lambert = max(dot(v_normal, flashlight_dir), 0.0);
	float phong = max(dot(v_normal, fvh), 0.0);
	//We can retrieve the distance term by calculating the difference vector between the fragment
	//and the light source and take that resulting vector's length.
	float distance    = length(u_flashlight_position - v_position);
	float attenuation = 1.0 / (u_flashlight_constant + u_flashlight_linear * distance +
    		    			   u_flashlight_quad * (distance * distance));
	/*
	Then we include this attenuation value in the lighting calculations
	by multiplying the attenuation value with the ambient, diffuse and specular colors.
	*/
	vec4 u_flashlight_color = attenuation *(intensity * u_flashlight_color);
	return u_flashlight_color * texture2D(u_tex_diffuse, v_uv) * lambert
			+ u_flashlight_color * texture2D(u_tex_specular, v_uv) * pow(phong, u_mat_shiny)
			+ (u_flashlight_color * 0.01);

}


void main(void)
{
	// If the player has is flashlight on, no need to include the players natural light around him
	if(use_flashlight>=0.0){
		gl_FragColor = calculate_directional_light();
		gl_FragColor += calculate_flashlight();
	}
	//If the player doesn't have his flashlight on give him a small light source around him
	if(use_flashlight==0.0){
	gl_FragColor = calculate_directional_light();
	gl_FragColor += calculate_light();
	}

}