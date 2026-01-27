Java.perform(function () {
    console.log("[*] Starting HTTP(s) interception...");

    // Intercept OkHttp3 requests and responses
    var OkHttpClient = Java.use('okhttp3.OkHttpClient');
    var Request = Java.use('okhttp3.Request');
    var Response = Java.use('okhttp3.Response');
    var Buffer = Java.use('okio.Buffer');

    var RealCall = Java.use('okhttp3.RealCall');
    RealCall.execute.implementation = function () {
        var request = this.request();

        console.log("\n[>] Intercepted HTTP request:");
        console.log("URL: " + request.url().toString());
        console.log("Method: " + request.method());
        console.log("Headers: " + request.headers().toString());

        // Try to get request body
        if (request.body() != null) {
            var buffer = Buffer.$new();
            request.body().writeTo(buffer);
            console.log("Request Body: " + buffer.readUtf8());
        } else {
            console.log("Request Body: <empty>");
        }

        var response = this.execute();

        console.log("\n[<] Intercepted HTTP response:");
        console.log("URL: " + request.url().toString());
        console.log("Code: " + response.code());
        console.log("Headers: " + response.headers().toString());

        // Try to get response body
        try {
            var responseBody = response.body().string();
            console.log("Response Body: " + responseBody);
        } catch (e) {
            console.log("Response Body: <could not read>");
        }

        return response;
    };
});
