import aspose.threed as a3d
scene = a3d.Scene.from_file('./data/cup15cm_test_6_PINHOLE_30000_1/cup15cm_test_6_PINHOLE_30000_1.obj')

scene.save('./data/cup15cm_test_6_PINHOLE_30000_1/cup15cm_test_6_PINHOLE_30000_1.ply')