package proxy;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Random;

@RestController
@RequestMapping("/api")
public class ProxyController {

    @Value("${MONOLITH_URL}")
    private String monolithUrl;

    @Value("${MOVIES_SERVICE_URL}")
    private String moviesServiceUrl;

    @Value("${GRADUAL_MIGRATION:true}")
    private boolean gradualMigration;

    @Value("${MOVIES_MIGRATION_PERCENT:50}")
    private int migrationPercent;

    @Value("${EVENTS_SERVICE_URL}")
    private String eventsServiceUrl;

    private final WebClient webClient = WebClient.create();
    private final Random random = new Random();

    @GetMapping("/movies/health")
    public Mono<ResponseEntity<String>> healthMoviesCheck() {
        String targetUrl = moviesServiceUrl + "/api/movies/health";
        return webClient.get()
                .uri(targetUrl)
                .retrieve()
                .toEntity(String.class);
    }

    @GetMapping("/movies")
    public Mono<ResponseEntity<String>> proxyMovies() {
        String targetUrl = monolithUrl + "/api/movies";
        if (gradualMigration) {
            int rand = random.nextInt(100);
            if (rand < migrationPercent) {
                targetUrl = moviesServiceUrl + "/api/movies";
            }
        }
        return webClient.get()
                .uri(targetUrl)
                .retrieve()
                .toEntity(String.class);
    }

    @PostMapping("/movies")
    public Mono<ResponseEntity<String>> proxyMoviesPost(@RequestBody String body) {
        String targetUrl = monolithUrl + "/api/movies";
        if (gradualMigration) {
            int rand = random.nextInt(100);
            if (rand < migrationPercent) {
                targetUrl = moviesServiceUrl + "/api/movies";
            }
        }
        return webClient.post()
                .uri(targetUrl)
                .bodyValue(body)
                .retrieve()
                .toEntity(String.class);
    }

    @PostMapping("/events/movie")
    public Mono<ResponseEntity<String>> proxyMovieEvent(@RequestBody String body) {
        String targetUrl = eventsServiceUrl + "/api/events/movie";
        return webClient.post()
                .uri(targetUrl)
                .bodyValue(body)
                .retrieve()
                .toEntity(String.class);
    }

    @PostMapping("/events/user")
    public Mono<ResponseEntity<String>> proxyUserEvent(@RequestBody String body) {
        String targetUrl = eventsServiceUrl + "/api/events/user";
        return webClient.post()
                .uri(targetUrl)
                .bodyValue(body)
                .retrieve()
                .toEntity(String.class);
    }

    @PostMapping("/events/payment")
    public Mono<ResponseEntity<String>> proxyPaymentEvent(@RequestBody String body) {
        String targetUrl = eventsServiceUrl + "/api/events/payment";
        return webClient.post()
                .uri(targetUrl)
                .bodyValue(body)
                .retrieve()
                .toEntity(String.class);
    }
}
