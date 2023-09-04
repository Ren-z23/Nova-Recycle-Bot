<?php
session_start();

// Set the username and password for manual login mode (change these values as needed)
$valid_username = 'guest';
$valid_password = 'password';

// Check if a token is provided in the URL
if (isset($_GET['token']) && !empty($_GET['token'])) {
    // Save the token in a session for later use
    $_SESSION['token'] = $_GET['token'];
}

// Handle login form submission
if (isset($_POST['username']) && isset($_POST['password'])) {
    // Get the submitted username and password
    $submitted_username = $_POST['username'];
    $submitted_password = $_POST['password'];

    // Perform manual login validation by comparing submitted credentials with valid credentials
    if ($submitted_username === $valid_username && $submitted_password === $valid_password) {
        // Successful login, store the username in the session
        $_SESSION['username'] = $valid_username;
    } else {
        // Invalid credentials, set the error flag to display an error message on the login form
        $error = true;
    }
}

// Check if the user is logged in
$is_logged_in = isset($_SESSION['username']);
?>

<!DOCTYPE html>
<html>

<head>
    <title>Login</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        #background-video {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }

        #login-form {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        #login-form label,
        #login-form input {
            display: block;
            margin-bottom: 10px;
        }

        #login-form input[type="submit"] {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        #login-form p.error-msg {
            color: red;
        }
    </style>
</head>

<body>
    <video id="background-video" autoplay muted loop>
        <source src="stock_video.mp4" type="video/mp4">
        <!-- Add additional video format sources if needed -->
        <!-- <source src="your_background_video_url.webm" type="video/webm"> -->
        <!-- <source src="your_background_video_url.ogv" type="video/ogg"> -->
        Your browser does not support the video tag.
    </video>

    <?php if (!$is_logged_in): ?>
        <!-- Show the login form if the user is not logged in -->
        <div id="login-form">
            <h2>Login</h2>
            <?php if (isset($error) && $error): ?>
                <p class="error-msg">Invalid credentials. Please try again.</p>
            <?php endif; ?>
            <form method="post" action="index.php">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <input type="submit" value="Login">
            </form>
        </div>
    <?php else: ?>
        <?php
        // Redirect to main_page.php if the user is logged in
        header('Location: main_page.php');
        exit;
        ?>
    <?php endif; ?>
</body>

</html>
