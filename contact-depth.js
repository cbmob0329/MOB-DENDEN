/* Keep seated art's screen size, but place its depth on a vertical world-space plane.
   The normal depth test remains enabled: foreground furniture still occludes it. */
window.ChillContactDepth={
 install(a){a.contactDepth={value:0};a.sprite.userData.contactDepth=a.contactDepth;a.sprite.material.onBeforeCompile=shader=>{shader.uniforms.chillContactDepth=a.contactDepth;shader.vertexShader='uniform float chillContactDepth;\n'+shader.vertexShader.replace('mvPosition.xy += rotatedPosition;', 'mvPosition.xy += rotatedPosition;\n mvPosition.z += chillContactDepth * rotatedPosition.y * viewMatrix[1][2] / max(0.25, viewMatrix[1][1]);');};a.sprite.material.customProgramCacheKey=()=> 'chill-upright-contact-v1';},
 update(a,pose){let seated=pose==='sit'||pose.startsWith('meal_')||pose.startsWith('bath_')||pose.startsWith('sit_')||pose.startsWith('excited_seated_wait_'),transition=['seating','toHome','staffSeating','staffReturning'].includes(a.cafeMode);a.contactDepth.value=seated?1:transition?Math.max(0,Math.min(1,a.pos.y/.48)):0;}
};
