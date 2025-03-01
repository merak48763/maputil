#version 150

bool roughlyEqual(float a, float b) {
  return abs(a - b) < 0.0001;
}

bool isGui(mat4 ProjMat) {
  return ProjMat[3][0] == -1.;
}

int getGuiScale(mat4 ProjMat, vec2 ScreenSize) {
  return int(round(ScreenSize.x * ProjMat[0][0] / 2.));
}
