#encoding:utf-8
import arcpy
import os

_sourcePath = 'D:\\工作相关\\arcgispro_py3\\arcgispro_py3.gdb'
arcpy.env.workspace = _sourcePath
if arcpy.Exists('result_point'):
    arcpy.Delete_management('result_point')
_publicLine = os.path.join(_sourcePath, 'publicLine')
_sourceFeature = ('FW')
_spatialReference = arcpy.Describe(_sourceFeature).spatialReference
arcpy.CreateFeatureclass_management(_sourcePath, 'result_point', 'POINT', '', '', '', _spatialReference)

with arcpy.da.SearchCursor(_sourceFeature, ['SHAPE@', 'OID@']) as cursor1:
    for row1 in cursor1:
        _polygon1List = []
        _polygon2List = []
        with arcpy.da.SearchCursor(_sourceFeature, ['SHAPE@', 'OID@']) as cursor2:
            for row2 in cursor2:
                # 根据属性判断相邻面
                if row1[0].touches(row2[0]):
                    # print(row1[1], row2[1])
                    # 相邻面相交获取公共边
                    print('OID:', row1[1], row2[1])
                    intersection_geom = row1[0].intersect(row2[0], 2)
                    # 遍历两个面的节点判断是否处于公共边上
                    for part1 in row1[0]:
                        for point1 in part1:
                            if point1:
                                _Point1 = arcpy.Point(point1.X, point1.Y)
                                _Point1Geometry = arcpy.PointGeometry(_Point1, 4490)
                                if _Point1Geometry.within(intersection_geom) or _Point1Geometry.touches(intersection_geom):
                                    # print('polygon1:', [point1.X, point1.Y])
                                    _polygon1List.append((round(point1.X, 5), round(point1.Y, 5)))
                    for part2 in row2[0]:
                        for point2 in part2:
                            if point2:
                                _Point2 = arcpy.Point(point2.X, point2.Y)
                                _Point2Geometry = arcpy.PointGeometry(_Point2, 4490)
                                if _Point2Geometry.within(intersection_geom) or _Point2Geometry.touches(intersection_geom):
                                    # print('polygon2:', [point2.X, point2.Y])
                                    _polygon2List.append((round(point2.X, 5), round(point2.Y, 5)))
                    # 比较两个面的公共边节点不同
                    print('_p1list:', _polygon1List)
                    print('_p2list:', _polygon2List)
                    # 仅在list1中出现的元素
                    unique_to_list1_ordered = [x for x in _polygon1List if x not in _polygon2List]
                    # print("仅在list1中:", unique_to_list1_ordered)

                    # 仅在list2中出现的元素
                    unique_to_list2_ordered = [x for x in _polygon2List if x not in _polygon1List]
                    # print("仅在list2中:", unique_to_list2_ordered)

                    # 将独有节点保存为矢量输出
                    with arcpy.da.InsertCursor(os.path.join(_sourcePath, 'result_point'), ['SHAPE@']) as cursor:
                        for xy in unique_to_list1_ordered:
                            point_geom = arcpy.PointGeometry(arcpy.Point(xy[0], xy[1]), 4490)
                            # print(point_geom)
                            cursor.insertRow([point_geom])
                        for xy in unique_to_list2_ordered:
                            point_geom = arcpy.PointGeometry(arcpy.Point(xy[0], xy[1]), 4490)
                            # print(point_geom)
                            cursor.insertRow([point_geom])

                    _polygon1List.clear()
                    _polygon2List.clear()

print('finish')



