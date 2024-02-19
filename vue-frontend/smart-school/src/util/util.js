import {ElNotification,ElMessageBox} from 'element-plus'
import nProgress from 'nprogress'



export function notice(message,type='info',title="提示信息",useHTML=false){
    ElNotification({
        title: title,
        message:message,
        type: type,
        dangerouslyUseHTMLString:useHTML,
        duration:3000
      })
}

export function msgbox(content="提示内容",title='Warning',type='Warning'){
  return ElMessageBox.confirm(
      content,
      title,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: type,
      }
    )
  }

  //显示全屏loading
  export function showLoading(){
    nProgress.start()
  }
  //隐藏全屏loading
  export function hideLoading(){
    nProgress.done()
  }

  // 将query对象转成url参数
export function queryParams(query){
  let q = []
  for (const key in query) {
      if(query[key]){
          q.push(`${key}=${encodeURIComponent(query[key])}`)
      }
  }
  let r = q.join("&")
  r = r ? ("?"+r) : ""
  return r
}

// 定义一个函数，无参数，输出为当前学年学期
export function getCurrentSemester () {
  let today = new Date ();
  let currentYear = today.getFullYear ();
  let startDate = new Date (currentYear, 8, 1); // 学期开始日期，假设为每年的 9 月 1 日
  let endDate = new Date (currentYear + 1, 5, 30); // 学期结束日期，假设为次年的 6 月 30 日
  if (startDate <= today && today <= endDate) {
    return `${currentYear}-${currentYear + 1} 学年 第一学期`;
  } else {
    return `${currentYear}-${currentYear + 1} 学年 第二学期`;
  }
}

export function dateToSemester (start, end) {
  let startDate = new Date (start);
  let endDate = new Date (end);
  let startYear = startDate.getFullYear ();
  let endYear = endDate.getFullYear ();
  let semester = "";
  if (startYear === endYear) {
    if (startDate.getMonth () >= 8 && endDate.getMonth () <= 5) {
      semester = `${startYear}-${startYear + 1} 学年 第一学期`;
    } else if (startDate.getMonth () <= 5 && endDate.getMonth () >= 6) {
      semester = `${startYear}-${startYear + 1} 学年 第二学期`;
    } else {
      semester = "无效的日期范围";
    }
  } else {
    if (endYear - startYear === 1) {
      if (startDate.getMonth () >= 8 && endDate.getMonth () <= 5) {
        semester = `${startYear}-${endYear} 学年 第一学期`;
      } else if (startDate.getMonth () <= 5 && endDate.getMonth () >= 6) {
        semester = `${endYear}-${endYear + 1} 学年 第二学期`;
      } else {
        semester = "无效的日期范围";
      }
    } else {
      semester = "无效的日期范围";
    }
  }
  return semester;
}