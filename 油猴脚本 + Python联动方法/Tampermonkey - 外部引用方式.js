// 基本配置
const server_url = "http://127.0.0.1:5000/"

// 工具窗口的设定
const tool_window = `
<style>
.twitter_tool {
      left: 10px;bottom: 10px;
      background: #1a59b7;
      color:#ffffff;
      overflow: hidden;
      z-index: 9999;
      position: fixed;
      padding:5px;
      text-align:center;
      width: 175px;
      height: 22px;
      display: table;
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 4px;
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
}
</style>
<div class="twitter_tool">
     <a id="tool_start_get_illustration" style="cursor: pointer;">开始获取插画</a><br>
     <a id="tool_stop_get_illustration" style="cursor: pointer;">停止获取插画</a>
</div>
`;


// 初始化变量
var setTimeout_tweet_tasks = [];  // 用于寻找推文的每一次循环任务
var setInterval_task = null;  // 用于布置任务的任务
var delay = 3000;  // 每次任务的延迟，不要太快，不然会加载失败。

// 输出调试信息

// 初始化工具悬浮窗口
$("body").append(tool_window);

// 绑定点击事件
$("#tool_start_get_illustration").click(function() {
    if (setInterval_task == null && setTimeout_tweet_tasks.length == 0) {
        console.log("开始获取插画！")
        // 反复检测是否需要再次寻找插画
        setInterval_task = setInterval(() => {
            if (setTimeout_tweet_tasks.length == 0) {
                console.log("一轮获取完毕，开始新的一轮......")
                get_tweet();
            }
        }, delay)  // 布置一次任务延迟
    }
});

$("#tool_stop_get_illustration").click(function() {
    console.log("已经执行停止获取插画的命令，请至少等待一分钟再开启获取插画功能！")
    // 终止布置任务
    clearInterval(setInterval_task);
    setInterval_task = null;
    // 终止每一次任务
    setTimeout_tweet_tasks.forEach((task) => {
        clearTimeout(task);
    })
});

// 定义获取函数
function get_tweet() {
    var cellInnerDivs = [];
    Array.from(document.getElementsByTagName("div")).forEach((div1) => {
        if (div1.dataset.testid == "cellInnerDiv"){
            cellInnerDivs.push(div1);
        }
    })
    if (cellInnerDivs.length == 0) {
        console.log("全部完毕！");
        // 终止布置任务
        clearInterval(setInterval_task)
        setInterval_task = null;
        return;
    }
    cellInnerDivs.forEach((div, index) => {
        setTimeout_tweet_tasks.push(setTimeout(() => {
            // 这里找推文内容
            Array.from(div.getElementsByTagName("div")).forEach((div_) => {
                if (div_.dataset.testid == "tweetText"){
                    console.log(div_.textContent);
                }
            })
            // 这里找推文图片
            Array.from(div.getElementsByTagName("img")).forEach((img) => {
                if (img.src.indexOf("pbs.twimg.com/media") != -1){
                    console.log(img.src);
                    var url = img.src;
                    // 处理 url 链接，获取最大的图片，就是原图
                    let pos = url.indexOf("?");
                    if (pos === -1) {
                        url += "?format=jpg&name=large";
                    } else {
                        url = url.slice(0, pos) + "?format=jpg&name=large";
                    }
                    GM_xmlhttpRequest({
                        url: server_url + "?url=" + btoa(url),  // base64编码传递
                        method :"GET",
                        headers: {},
                        onload:function(xhr){
                            //console.log(xhr.responseText);
                        }
                    });
                }
            })
            div.remove();
            setTimeout_tweet_tasks.shift();  // 弹出一个
        }, delay * index));  // 设置了一个延迟，不能太快
    })

}

