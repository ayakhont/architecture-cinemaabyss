package proxy;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest
@TestPropertySource(properties = {
        "MONOLITH_URL=http://monolith:8080",
        "MOVIES_SERVICE_URL=http://movies-service:8081",
        "GRADUAL_MIGRATION=true",
        "MOVIES_MIGRATION_PERCENT=50"
})
class ProxyServiceApplicationTest {
    @Test
    void contextLoads() {
        // Verifies that the Spring context loads successfully
    }
}

