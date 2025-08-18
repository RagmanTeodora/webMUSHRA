<?php
/*************************************************************************
 (C) Copyright AudioLabs 2017

This source code is protected by copyright law and international treaties. This source code is made available to You subject to the terms and conditions of the Software License for the webMUSHRA.js Software. Said terms and conditions have been made available to You prior to Your download of this source code. By downloading this source code You agree to be bound by the above mentionend terms and conditions, which can also be found here: https://www.audiolabs-erlangen.de/resources/webMUSHRA. Any unauthorised use of this source code may result in severe civil and criminal penalties, and will be prosecuted to the maximum extent possible under law.

**************************************************************************/

// Function to sanitize data, from original script
function sanitize($string = '', $is_filename = FALSE)
{
 // Replace all weird characters with dashes
 $string = preg_replace('/[^\w\-'. ($is_filename ? '~_\.' : ''). ']+/u', '-', $string);
 // Only allow one dash separator at a time (and make string lowercase)
 return strtolower(preg_replace('/--+/u', '-', $string));
}

// Get the POST data from the MUSHRA test
$sessionParam = null;
if(version_compare(PHP_VERSION, '8.0.0', '<') and get_magic_quotes_gpc()){
    $sessionParam = stripslashes($_POST['sessionJSON']);
}else{
    $sessionParam = $_POST['sessionJSON'];
}

$session = json_decode($sessionParam);

// --- START: Email Logic ---

// Your email address
$to = 'youremail@example.com'; 
$subject = 'MUSHRA Test Results for ' . $session->testId;

// Build the email body
$body = "New test results received!\n\n";
$body .= "Test ID: " . $session->testId . "\n";
$body .= "Participant Name: " . $session->participant->response->name . "\n";
$body .= "Email: " . $session->participant->response->eMail . "\n";
$body .= "Age: " . $session->participant->response->age . "\n";
$body .= "Gender: " . $session->participant->response->gender . "\n\n";

$body .= "--- MUSHRA Scores ---\n";
foreach ($session->trials as $trial) {
    if ($trial->type == "mushra") {
        $body .= "Trial: " . $trial->id . "\n";
        foreach ($trial->responses as $response) {
            $body .= "  " . $response->stimulus . ": " . $response->score . " (Time: " . $response->time . ")\n";
        }
        if (isset($trial->comment) && !empty($trial->comment)) {
            $body .= "  Comment: " . $trial->comment . "\n";
        }
    }
}

// Send the email
if (mail($to, $subject, $body)) {
    echo "Results successfully emailed!";
} else {
    echo "Error: Could not send email.";
}
// --- END: Email Logic ---

?>