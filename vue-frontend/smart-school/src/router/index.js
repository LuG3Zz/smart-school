import {
    createRouter,
    createWebHashHistory
} from 'vue-router'

import Index from "~/pages/index.vue"
import Student from "~/layout/student.vue"
import NotFound from "~/pages/404.vue"
import Login from "~/pages/login.vue"
import Create from "~/pages/create.vue"
import PersonInfo from "~/pages/student/personinfo.vue"
import SecuritySetting from "~/pages/student/securitysetting.vue"
import AcademicInfo from "~/pages/student/academicinfo.vue"
import AffairsApplication from "~/pages/student/affairsapplication.vue"
import AffairsinQuiry from "~/pages/student/affairsinquiry.vue"
import DormitoryInfoy from "~/pages/student/dormitoryinfoy.vue"
import StayApplication from "~/pages/student/stayapplication.vue"
import RepairRequest from "~/pages/student/repairrequest.vue"
import CourseInfo from "~/pages/student/coursesinfo.vue"
import StudentsList from "~/pages/studentadmin/studentlist.vue"
import StudentCourseManager from "~/pages/studentcourse/coursemanager.vue"
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
        path: "/personal-info",
        name: "/personal-info",
        component: PersonInfo,
        meta: {
            title: "个人信息"
        }
    },
    {
        path: "/academic-info",
        name: "/academic-info",
        component: AcademicInfo,
        meta: {
            title: "学业信息"
        }
    },
    {
        path: "/security-settings",
        name: "/security-settings",
        component: SecuritySetting,
        meta: {
            title: "安全设置"
        }
    },
    {
        path: "/affairs-application",
        name: "/affairs-application",
        component: AffairsApplication,
        meta: {
            title: "事务申请"
        }
    },
    {
        path: "/affairs-inquiry",
        name: "/affairs-inquiry",
        component: AffairsinQuiry,
        meta: {
            title: "申请查询"
        }
    },
    {
        path: "/dormitory-info",
        name: "/dormitory-info",
        component: DormitoryInfoy,
        meta: { title: "宿舍信息" }
    },
    {
        path: "/repair-request",
        name: "/repair-request",
        component: RepairRequest,
        meta: { title: "报修服务" }
    },
    {
        path: "/stay-application",
        name: "/stay-application",
        component: StayApplication,
        meta: { title: "假期留校申请" }
    },
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
