$(document).ready(function () {
    py_title(function (title) {
        $('#title').text(title)
    })


    let form = $('.form-signin')
    // 处理提交事件
    form.submit(function (e) {
        e.preventDefault();
        let param = form.serialize().split('&')
        let py_param = {}
        param.forEach((item) => {
            const temp = item.split('=')
            py_param[temp[0]] = temp[1]
        })
        // 调用python函数登录, 并返回登录状态和错误信息
        py_login(py_param, function (status, err) {
            if (status) {
                iziToast.success({
                    title: '提示',
                    message: '登录成功.',
                    position: 'bottomRight',
                    transitionIn: 'bounceInLeft',
                    timeout: 1000,
                    onClosed: function () {
                        location.href = './main.html'
                    }
                });
            } else {
                iziToast.warning({
                    title: '提示',
                    message: '登录失败. ' + err,
                    position: 'bottomRight',
                    transitionIn: 'bounceInLeft'
                });
            }
        })

    })

    // 处理标题栏拖动
    let mouse_isDown = false
    const header = 'header'//拖动对象名称
    $(header).mousedown(function (e) {
        mouse_isDown = true;
    });
    $(header).mouseup(function (e) {
        mouse_isDown = false;
    });

    $(header).mouseleave(function (e) {
        mouse_isDown = false;
    });
    $(header).mousemove(function (e) {
        if (mouse_isDown) {
            py_move()
        }
    });
});
