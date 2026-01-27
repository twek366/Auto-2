console.log("[+] Starting with root checks...");


Java.perform(function() {
    try {
        const Process = Java.use("android.os.Process");
        if (Process.myUid() === 0) {
            console.log("[+] Running as root!");
        } else {
            console.log("[-] NOT running as root!");
        }
    } catch (e) {
        console.log("[-] Root check failed: " + e);
    }
});


try {
    const sslRead = Module.findExportByName("libssl.so", "SSL_read");
    if (!sslRead) throw new Error("libssl.so not found");

    Interceptor.attach(sslRead, {
        onLeave: function(retval) {
            try {
                const data = this.buf.readByteArray(retval.toInt32());
                console.log(hexdump(data));
            } catch (e) {
                console.log("[-] SSL_read error: " + e);
            }
        }
    });
} catch (e) {
    console.log("[-] Global error: " + e);
}