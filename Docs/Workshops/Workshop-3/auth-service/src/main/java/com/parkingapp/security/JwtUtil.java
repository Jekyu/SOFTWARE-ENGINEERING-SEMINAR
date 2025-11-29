package com.parkingapp.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtParser;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import io.jsonwebtoken.JwtParser;
import io.jsonwebtoken.Jwts;
import java.util.Base64;
import java.util.Date;

@Component
public class JwtUtil {

    @Value("${app.jwt.secret}")
    private String secret;

    @Value("${app.jwt.expiration-ms}")
    private long expirationMs;

    private String secretKey;

    @PostConstruct
    public void init() {
        this.secretKey = Base64.getEncoder().encodeToString(secret.getBytes());
    }

    public String generateToken(String subjectEmail) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + expirationMs);

        return Jwts.builder()
                .setSubject(subjectEmail)
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(SignatureAlgorithm.HS256, secretKey)
                .compact();
    }

    private Claims getClaims(String token) {
        JwtParser parser = Jwts.parserBuilder()
                .setSigningKey(secretKey)
                .build();

        return parser.parseClaimsJws(token).getBody();
    }

    public String extractUsername(String token) {
        // aquí devuelve el email, porque lo usamos como subject
        return getClaims(token).getSubject();
    }

    public boolean validateToken(String token) {
        try {
            getClaims(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
