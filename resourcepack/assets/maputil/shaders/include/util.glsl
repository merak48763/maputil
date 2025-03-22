#version 150

#ifndef PI
#define PI (3.1415926535897932384626433832795)
#endif
#ifndef TAU
#define TAU (6.283185307179586476925286766559)
#endif

bool roughlyEqual(float a, float b) {
  return abs(a - b) < 0.0001;
}

bool isGui(mat4 ProjMat) {
  return ProjMat[3][0] == -1.;
}

float getGuiScale(mat4 ProjMat, vec2 ScreenSize) {
  return round(ScreenSize.x * ProjMat[0][0] / 2.);
}
