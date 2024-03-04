import {
    createRouter,
    createWebHashHistory
} from 'vue-router'

import Index from "~/pages/index.vue"
import Student from "~/layout/student.vue"
import NotFound from "~/pages/404.vue"
import Login from "~/pages/login.vue"
import Create from "~/pages/create.vue"
import CourseSelection from "~/pages/student/CourseSelection/courseselection.vue"
import Discipline from "~/pages/student/discipline/discipline.vue"
import CourseInfo from "~/pages/student/coursesinfo.vue"
import StudentsList from "~/pages/studentadmin/studentlist.vue"
import StudentCourseManager from "~/pages/studentcourse/coursemanager.vue"
import Departmentinfo from "~/pages/departmenthead/departmentlist.vue"
import MyCourseInfo from "~/pages/teacher/coursemanager.vue"
import AffairsRecord from "~/pages/affairsrecord/list.vue"
import NotificationList from "~/pages/notification/list.vue"
import LeaveSchool from "~/pages/leave_school/list.vue"
import StudentAnalytics from "~/pages/studentanalytics/index.vue"
import DormitoryInfo from "~/pages/dormitory/list.vue"
import Info from "~/pages/info.vue"

import ImageList from "~/pages/image/list.vue"

const routes = [
    {
        path: "/",
        name:"Student",
        component: Student,
        children:[{
            path: "/",
            name: "/",
            component: Index,
            meta: { title: "首页" }
        },
    ]
        
    },
    {
        path:"/login",
        component:Login,
        meta:{
            title:"登录页"
        }

    },
    {
        path:"/create",
        component:Create,
        meta:{
            title:"注册页"
        }

    },
    {
        path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound
    },
]
 
//动态路由，匹配菜单动态添加路由
const asyncRoutes=
    [
                            
    {
        path: "/students-list",
        name: "/students-list",
        component: StudentsList,
        meta: { title: "学生列表" }
    },
    {
        path: "/course-manager",
        name: "/course-manager",
        component: StudentCourseManager,
        meta: { title: "课程管理列表" }
    },
    {
        path: "/courses-info",
        name: "/courses-info",
        component: CourseInfo,
        meta: { title: "课程管理列表" }
    },
    {
        path: "/departments-info-view",
        name: "/departments-info-view",
        component: Departmentinfo,
        meta: { title: "院系管理列表" }
    },
    {
        path: "/my-course-info-view",
        name: "/my-course-info-view",
        component: MyCourseInfo,
        meta: { title: "管理的课程" }
    },
    {
        path: "/course-selection",
        name: "/course-selection",
        component: CourseSelection,
        meta: { title: "课程选择" }
    },
    {
        path: "/discipline-search",
        name: "/discipline-search",
        component: Discipline,
        meta: { title: "课程选择" }
    },
    {
        path: "/affairs-record",
        name: "/affairs-record",
        component: AffairsRecord,
        meta: { title: "事务记录" }
    },
    {
        path: "/image",
        name: "/image",
        component: ImageList,
        meta: { title: "资料管理" }
    },
    {
        path: "/notification",
        name: "/notification",
        component: NotificationList,
        meta: { title: "通知列表" }
    },
    {
        path: "/checkout-process",
        name: "/checkout-process",
        component: LeaveSchool,
        meta: { title: "离校管理" }
    },
    {
        path: "/student-analytics",
        name: "/student-analytics",
        component: StudentAnalytics,
        meta: { title: "学生分析" }
    },
    {
        path: "/dormitory-info",
        name: "/dormitory-info",
        component: DormitoryInfo,
        meta: { title: "宿舍信息" }
    },
    {
        path: "/info",
        name: "/info",
        component: Info,
        meta: { title: "个人信息" }
    },


    ]





 export const router = createRouter({
    history: createWebHashHistory(),
    routes,

})

//动态添加路由的方法
export function addRoutes(menus){
    //是否有新路由
    let hasNewRoutes = false
    const AddRouterByMenus = (arr) => {
        arr.forEach(element => {
            let item = asyncRoutes.find(o=>o.path == element.href)
            if(item && !router.hasRoute(item.path)){
                router.addRoute("Student",item)
                hasNewRoutes = true
            }
            if(element.children && element.children.length>0 ){
                AddRouterByMenus(element.children)
            }

            
        });
    }
    AddRouterByMenus(menus)
    return hasNewRoutes
}
