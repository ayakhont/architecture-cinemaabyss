package proxy;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.TestPropertySource;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClient.ResponseSpec;
import reactor.core.publisher.Mono;
import org.springframework.http.ResponseEntity;

@WebFluxTest(proxy.ProxyController.class)
@TestPropertySource(properties = {
        "MONOLITH_URL=http://monolith:8080",
        "MOVIES_SERVICE_URL=http://movies-service:8081",
        "GRADUAL_MIGRATION=true",
        "MOVIES_MIGRATION_PERCENT=50"
})
class ProxyControllerTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private WebClient webClient;

    @Test
    void proxyMoviesReturnsResponse() {
        WebClient.RequestHeadersUriSpec uriSpec = Mockito.mock(WebClient.RequestHeadersUriSpec.class);
        WebClient.RequestHeadersSpec headersSpec = Mockito.mock(WebClient.RequestHeadersSpec.class);
        ResponseSpec responseSpec = Mockito.mock(ResponseSpec.class);

        Mockito.when(webClient.get()).thenReturn(uriSpec);
        Mockito.when(uriSpec.uri(Mockito.anyString())).thenReturn(headersSpec);
        Mockito.when(headersSpec.retrieve()).thenReturn(responseSpec);
        Mockito.when(responseSpec.toEntity(String.class)).thenReturn(Mono.just(ResponseEntity.ok("mocked response")));

        webTestClient.get()
                .uri("/api/movies")
                .exchange()
                .expectStatus().is5xxServerError();
    }
}
