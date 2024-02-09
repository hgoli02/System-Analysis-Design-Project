import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

public class JavaClient {
    private String serverUrl;
    private HttpClient client;

    public JavaClient(String serverUrl, int port) {
        this.serverUrl = "localhost".equals(serverUrl) ? "http://127.0.0.1:" + port : serverUrl;
        this.client = HttpClient.newHttpClient();
    }

    public void push(String key, String value) {
        try {
            String message = key + "," + value;
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(serverUrl + "/push"))
                    .POST(BodyPublishers.ofString(message))
                    .build();
            HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
            System.out.println("Received from server: " + response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void pull() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(serverUrl + "/pull"))
                    .GET()
                    .build();
            HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
            System.out.println("Received from server: " + response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void subscribeRunner(String url, Consumer<String> f) {
        Executors.newSingleThreadExecutor().submit(() -> {
            while (true) {
                try {
                    HttpRequest request = HttpRequest.newBuilder()
                            .uri(URI.create(url + "/pull"))
                            .GET()
                            .build();
                    HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
                    String data = response.body();
                    if (!"no message".equals(data)) {
                        f.accept(data);
                    } else {
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void subscribe(Consumer<String> f) {
        subscribeRunner(serverUrl, f);
    }

    public static void main(String[] args) {
        JavaClient client = new JavaClient("localhost", 8000);
        client.subscribe(data -> System.out.println("Received data: " + data));
        // Example usage
        client.push("key", "value");
        client.push("key", "value2");

    }
}
