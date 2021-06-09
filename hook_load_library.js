function showStacks() {
    var output="";
    Java.perform(function () {
        output= Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new());
        console.log(output);
    });
    return output;
}
function getStacks() {
    var output="";
    Java.perform(function () {
        output=Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new())
    });
    return output;
}
Java.perform(function () {
    var system=Java.use("java.lang.System");
    const Runtime = Java.use('java.lang.Runtime');
    const VMStack = Java.use('dalvik.system.VMStack');
    system.loadLibrary.implementation=function(arg){
        console.log("hooked in loadLibrary");
        console.log(arg);
        send("block");
        var op=recv("input",function(){});
        op.wait();
        const ret = Runtime.getRuntime().loadLibrary0(VMStack.getCallingClassLoader(), arg);
        return ret;
    }
});