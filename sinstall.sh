#!/bin/bash

# 考虑到在平时工作中包名一般不会改变，就把包名写死在脚本中，从而简化了调用脚本的参数
# 根据自身情况更改相应包名，否则卸载和清空数据功能不能正常使用
packageName="com.sun.example"

# 输出命令提示
function printTips() {
    #statements
    echo "usage: sinstall [-u] <productFlavors> <buildTypes>"
    echo "usage: sinstall [-c | --help]"
    echo ""
    echo "                -u     -- unistall existing application"
    echo "                -c     -- clear existing application data"
    echo "                --help -- display help message"
}

# 打包并安装 参数1:productFlavor 参数2:buildType
function buildAndInstallApp() {
    echo "开始打包..."
    productFlavor=$1
    buildType=$2
    # 将productFlavor第一位转成大写
    assembleProductFlavor=$(echo ${productFlavor:0:1} | tr '[a-z]' '[A-Z]')${productFlavor:1:${#productFlavor}}
    # 将buildType第一位转成大写
    assembleBuildType=$(echo ${buildType:0:1} | tr '[a-z]' '[A-Z]')${buildType:1:${#buildType}}
    # 拼接assemble命令
    assembleCommond=`./gradlew assemble$assembleProductFlavor$assembleBuildType`
    result=${assembleCommond}
    if [[ "$result" =~ "SUCCESSFUL" ]];
    then
        echo "打包成功"
        # 安装
        installApp $productFlavor $buildType;
    else
        echo "打包失败"$result
        # 语音提示
        say 蓝瘦 香菇
    fi
}

# 安装 参数1:productFlavor 参数2:buildType
function installApp() {
    echo "开始安装..."
    # 根据productFlavor和buildType拼接出目标apk名字
    targetApkName=app-$1-$2".apk"
    # 拼接安装命令
    installCommond=`adb install -r ./app/build/outputs/apk/$targetApkName`
    result=${installCommond}
    if [[ "$result" =~ "Success" ]];
    then
        echo "安装成功"
        # 语音提示
        say 美滋滋
    else
        # 提取有效错误信息，并输出
        IFS=' ' arr=($result)
        echo "安装失败"${arr[${#arr[*]}-1]}
        # 语音提示
        say 蓝瘦 香菇
    fi
}

# 卸载 参数1:包名
function uninstallApp() {
    echo "开始删除应用..."
    uninstallCommond=`adb uninstall $1`
    result=${uninstallCommond}
    if [[ "$result" =~ "Success" ]];
    then
        echo "删除成功"
    else
        echo "删除失败"$result
    fi
}

# 清空数据 参数1:包名
function clearAppData() {
    echo "开始清空数据..."
    uninstallCommond=`adb shell pm clear $1`
    result=${uninstallCommond}
    if [[ "$result" =~ "Success" ]];
    then
        echo "清空成功"
    else
        echo "清空失败"$result
    fi
}

if [ $# -le 0 ]
then
    printTips
    exit 0
fi

if [ $# -eq 1 ]
then
    if [ $1 == "-c" ]
    then
        clearAppData $packageName;
    elif [ $1 == "--help" ]
    then
        printTips
    else
        printTips
    fi
exit 0
fi

# 脚本模式 0:覆盖安装 1:卸载旧包，重新安装
scriptMode=0
productFlavor="$1"
buildType="$2"

if [ $1 == "-u" ]
then
    scriptMode=1
    productFlavor="$2"
    buildType="$3"
fi

if [ $1 == "-c" ]
then
    scriptMode=2
    productFlavor="$2"
    buildType="$3"
fi

if [ $scriptMode -eq 1 ]
then
    # 卸载旧的应用
    uninstallApp $packageName;
fi

# 打包并安装
buildAndInstallApp $productFlavor $buildType;

echo "结束"
