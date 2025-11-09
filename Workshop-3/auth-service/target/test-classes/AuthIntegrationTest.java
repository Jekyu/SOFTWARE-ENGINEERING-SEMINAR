package com.parkingapp;

import com.parkingapp.dto.LoginRequest;
import com.parkingapp.dto.RegisterRequest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.*;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class AuthIntegrationTest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void testRegisterAndLogin() {
        String baseUrl = "http://localhost:" + port + "/api/auth";

        // Registrar usuario
        RegisterRequest register = new RegisterRequest();
        register.setUsername("userTest");
        register.setPassword("password123");
        register.setEmail("user@test.com");
        register.setAccessCode("REGISTER-2025-01");

        ResponseEntity<String> registerResponse =
                restTemplate.postForEntity(baseUrl + "/register", register, String.class);

        assertThat(registerResponse.getStatusCode()).isEqualTo(HttpStatus.OK);

        // Iniciar sesión
        LoginRequest login = new LoginRequest();
        login.setUsername("userTest");
        login.setPassword("password123");

        ResponseEntity<String> loginResponse =
                restTemplate.postForEntity(baseUrl + "/login", login, String.class);

        assertThat(loginResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(loginResponse.getBody()).contains("token");
    }
}
