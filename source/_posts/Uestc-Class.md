---
title: Uestc抢课脚本
date: 2018-03-10 11:36:37
tags: [Script,Python]
---
# 一个电子科大的模块

### 涉及登录，查分，抢课等功能



---

 - `import uestc`  *导入文件*
 
 -  `session=uestc.login(studentId,password)` 生成 *`session`* 登录
 
 -  - `termId=uestc.query.get_now_semesterid(session)`     查询当前学期 *`Id`*
  -   `entrance=uestc.catch_course.get_open_entrance(session)` 获取选课通道，返回通道 *`list`*
  - `class_Id_List=uestc.catch_course.get_entrance_class(session,entrance)` 获取选课列表 
  
 - `flag=uestc.catch_course.catch_course(session, entrance_list,class_id_list)` 返回值若为 `0` 表示抢课成功 


  


---

[1] [Uestc抢课脚本][1]


  [1]: https://github.com/plusIs/uestc