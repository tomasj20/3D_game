varying vec4 v_color;
varying vec2 v_uv;
uniform sampler2D u_tex_diffuse;

void main(void)
{
    gl_FragColor = texture2D(u_tex_diffuse, v_uv);
    //glFragColor = v_color;
}