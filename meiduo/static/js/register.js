/**
 * Created by python on 20-9-4.
 */
//创建vm的vue对象
var vm = new Vue({
    el: "#app",
    //修改Vue读取变量的方法
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',
        password2: '',
        mobile: '',
        image_code_url: '',
        uuid: '',
        image_code: '',
        sms_code_tip: '获取短信验证码',
        send_flg : false,   //是否已经发送短信验证码
        //v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        //error_message
        error_name_message: '',
        error_mobile_message: '',
        error_image_code_message: ''
    },
    //页面一加载完，vue自动调用mounted函数
    mounted(){
        //生成图形验证码
        this.generate_image_code();
    },
    methods: {
        // 生成图形验证码的方法：封装思想，代码复用
        generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
        },
        //校验用户名
        check_username(){
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }

            //判断用户名是否重复
            if (this.error_name == false) {
                //只有当用户输入的用户名满足条件时，才会继续
                //两个参数，一个请求地址，一个请求头
                let url = '/usernames/' + this.username + '/count/';
                axios.get(url, {
                    responseType: 'json',
                }).then(response => {
                    if (response.data.count == 1) {
                        //用户名已存在
                        this.error_name_message = '用户名已存在';
                        this.error_name = true;
                    }
                    else {
                        //用户名不存在
                        this.error_name = false;
                    }
                }).catch(error => {
                    console.log(error.response);
                });
            }
        },
        //校验密码
        check_password(){
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        //校验确认密码
        check_password2(){
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        //校验手机号
        check_mobile(){
            //console.log(this.mobile);
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }

            //校验手机号是否重复
            if (this.error_mobile == false) {
                let url = '/mobile/' + this.mobile + '/count/'
                axios.get(url, {
                    responseType: 'json',
                }).then(response => {
                    if (response.data.count == 1) {
                        this.error_mobile_message = '此电话号码已存在';
                        this.error_mobile = true;
                    }
                    else {
                        this.error_mobile = false;
                    }
                }).catch(error => {
                    console.log(error.response);
                })
            }
        },
        check_image_code(){
            if (this.image_code.length < 4) {
                this.error_image_code_message = "请输入四位图形验证码";
                this.error_image_code = true;
            }
            else {
                this.error_image_code = false;
            }
        },
        //校验协议勾选
        check_allow(){
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        //发送短信验证码
        send_sms_code(){
            //避免用户频繁点击获取验证码的标签
            if(this.send_flg == true){
                return
            }
            this.send_flg = false;
            //校验mobile和image_code
            this.check_mobile();
            this.check_image_code();
            if(this.error_mobile == true || this.error_image_code == true){
                return;
            }

            let url = "/sms_codes/" + this.mobile + "/?image_code=" + this.image_code + "&uuid=" + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        //展示倒计时60s,创建一个计时器
                        //setInterval('回调函数','时间间隔');
                        let num = 60;
                        let no = setInterval(() =>{
                            if(num == 1){//倒计时即将结束
                                //停止会掉函数的执行
                                clearInterval(no);
                                //还原sms_code_tip
                                this.sms_code_tip = '获取短信验证码';
                                //重新生成图形验证码
                                this.generate_image_code();
                            }
                            else{
                                num -= 1;
                                this.sms_code_tip = num + '秒';
                            }
                        },1000);
                    }
                    else {
                        if (response.data.code == "4001") {
                            //图形验证码有误
                            this.error_image_code_message = response.data.errmsg;
                            this.error_image_code = true;
                        }
                    }
                })
                .catch(error => {
                    console.log(error.response)
                })
        },
        //提交事件
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();

            if (this.error_name == true || this.error_password == true || this.error_password2 == true
                || this.error_mobile == true || this.error_allow == true) {
                // 禁用表单的提交
                window.event.returnValue = false;
            }
        },
    }
});