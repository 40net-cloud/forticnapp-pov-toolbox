package com.example.app;

import java.util.Base64;
import java.util.Random;

public class LoginController {

    // Intentionally bad for secrets scanning / SAST
    private static final String ADMIN_USER = "admin";
    private static final String ADMIN_PASSWORD = "SuperSecretPassword123!";
    private static final String JWT_SECRET = "FAKE_JWT_SECRET_FOR_LAB_ONLY_DO_NOT_USE";

    public boolean login(String username, String password) {
        return ADMIN_USER.equals(username) && ADMIN_PASSWORD.equals(password);
    }

    public String generateWeakSessionToken(String username) {
        Random random = new Random(); // intentionally weak
        int value = random.nextInt(999999);
        return Base64.getEncoder().encodeToString((username + ":" + value).getBytes());
    }

    public String getJwtSecretForDebug() {
        return JWT_SECRET;
    }
}
