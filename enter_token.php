<?php
session_start();

// Check if the user is logged in, if not, redirect to index.php
if (!isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}

// Check if the $login_mode is provided in the URL
if (isset($_GET['login_mode'])) {
    $login_mode = $_GET['login_mode'];
} else {
    // Set a default value for $login_mode in case it's not provided
    $login_mode = 'manual'; // You can change this to 'auto' if needed
}

// Valid tokens (replace these with your actual valid tokens)
$valid_tokens = array(
    'token1',
    'token2',
    'token3'
);

// Initialize the error message
$error_msg = '';

// Check if a token is provided in the URL or from the form submission
if (isset($_POST['token']) && !empty($_POST['token'])) {
    // Save the token in a session for later use
    $_SESSION['token'] = $_POST['token'];

    // Check if the entered token is valid (in the list of valid tokens)
    if (in_array($_SESSION['token'], $valid_tokens)) {
        // Valid token, process it here if needed
        $processed_token = $_SESSION['token'];
    } else {
        // Invalid token, set an error message
        $error_msg = 'Invalid token. Please try again.';
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Enter Token</title>
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

        #enter-token-form {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        #enter-token-form label,
        #enter-token-form input {
            display: block;
            margin-bottom: 10px;
        }

        #enter-token-form input[type="submit"] {
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

        #enter-token-form p.error-msg {
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

    <div id="enter-token-form">
        <h2 style="text-align: center;">Welcome, <?php echo $_SESSION['username']; ?>!</h2>
        <p style="text-align: center;">Please enter your token:</p>
        <form method="post" action="enter_token.php" style="text-align: center;">
            <input type="text" name="token" required value="<?php echo isset($_SESSION['token']) ? $_SESSION['token'] : ''; ?>">
            <br>
            <input type="submit" value="Submit">
        </form>

        <?php if ($error_msg !== ''): ?>
            <p style="text-align: center; color: red;"><?php echo $error_msg; ?></p>
        <?php endif; ?>

        <?php if (isset($processed_token)): ?>
            <p style="text-align: center;">Token processed: <?php echo $processed_token; ?></p>
            <p style="text-align: center;">You are rewarded 30 points!</p>
        <?php endif; ?>
    </div>
</body>
</html>