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