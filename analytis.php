<?php
include 'php_functions.php';

//Establishing user id
session_start();
$user_id = id_maker();

// Setting up the HTML page and aesthetics
echo "<html lang = 'en'>";
echo "<link rel = 'stylesheet' href = 'aesthetics2.css'>";	

// Setting up the navigation bar
	echo "<h1 class = 'site title'>PROTEIGNOSIA</h1>";
	echo "<div class = 'navbar'>";
                echo "<a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/analytis.php'>Home</a>";
                echo "<a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/statement_of_credit.html'>Statement of Credit</a>";
        echo "</div>";
echo "<body>";
		echo "<h4>Protei-: derived from 'proteios' (πρωτεῖος), Greek for 'primary'</h4>";
		echo "<h4>-gnosia: from 'gnosis'(γνῶσις), Greek for 'understanding'</h4>";
		echo "<h2>Proteignosia: the understanding/study of proteins</h2><br>";
		echo "<h4>To conduct your study, please enter the protein information and the analyses you would like to conduct.</h4>";

		//Setting up the form to retrieve the protein and taxonomic information
		echo "<form action = 'analytis.php' method = 'post'>";
		echo "<fieldset>";
		echo "<legend>Protei</legend>";
		echo	"<label>Protein family: <input type = 'text' name = 'prot_family'></label><br>";
		echo	"<label>Taxonomic group:<input type = 'text' name = 'taxon_group'></label><br>";
		echo "</fieldset>";

		echo "<fieldset>";	
		echo "<legend>Gnosia</legend>";
		echo "<input type='checkbox' id='MSA' name='test1' value='1'>";
		echo "<label for='MSA'>Multiple Sequence Alignment</label><br>";
		echo "<input type = 'checkbox' id = 'PD' name = 'test2' value = '1'>";
                echo "<label for='PS'> Search for PROSITE Domains</label><br>";
		echo "<input type = 'checkbox' id = 'PS' name = 'test3' value = '1'>";
		echo "<label for='PS'> Protein Statistics Report</label><br>";
		echo "</fieldset>";
		echo  "<input type='submit' value='Submit'>";
		echo "</form>";
		echo "</html>";

//Collecting the input from the Analytis form and creating it as output to feed into the backend_python.py file
if(isset($_POST['prot_family']) && isset($_POST['taxon_group'])){
	
	//For Part1:
	
	$protein_family = str_replace(' ', '_', $_POST['prot_family']);
	echo "$protein_family";
	#$protein_family = preg_replace('/[^\w\s\-.,]/u', '', $protein_family); // Safer sanitization
	
	$taxonomic_group = str_replace(' ', '_', $_POST['taxon_group']);
	echo "$taxonomic_group";
	#$taxonomic_group = preg_replace('/[^\w\s\-.,]/u', '', $taxonomic_group);
	##$taxonomic_group = preg_replace('/[^a-zA-Z0-9 _-]/', '', $_POST['taxon_group']);
	
	//$protein_family = preg_replace('/[^a-zA-Z0-9 _-]/', '', $_POST['prot_family']);
	//$taxonomic_group = preg_replace('/[^a-zA-Z0-9 _-]/', '', $_POST['taxon_group']);
	//$protein_family = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['prot_family']);
	//$taxonomic_group = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['taxon_group']);
	//For Part 2:
	$MSAtest = isset($_POST['test1']) ? '1' : '0';
	//For Part 3:
	$PDreport = isset($_POST['test2']) ? '1' : '0';
	// For Part 4:
	$PSreport = isset($_POST['test3']) ? '1' : '0';

//Executing the python code -> relevant to all parts
	#$python_run = "python3 /home/s2103976/public_html/ICA/backend_python.py " .escapeshellarg($protein_family) . " " . escapeshellarg($taxonomic_group) . " " . $MSAtest . " " . $PDreport . " " . $PSreport;
	#$python_run = "python3 /home/s2103976/public_html/ICA/backend_python.py $protein_family $taxonomic_group $MSAtest  $PDreport $PSreport";
	 $python_run = escapeshellcmd("python3 /home/s2103976/public_html/ICA/backend_python.py") . " " . escapeshellarg($protein_family) . " " . escapeshellarg($taxonomic_group) . " " . escapeshellarg($MSAtest) . " " . escapeshellarg($PDreport) . " " . escapeshellarg($PSreport);
	$run_python_run = shell_exec($python_run);

	echo "<pre>$run_python_run</pre>";

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['prot_family']) && !empty($_POST['taxon_group'])) {
    $filename = $taxonomic_group . '_' . $protein_family . '_results.zip';
    $filepath = '/home/s2103976/public_html/ICA/' . $filename;

    sleep(2);

    if (file_exists($filepath)) {
    
	echo "<h4>Your data awaits...</h4>";    
	echo "<div class='button-container'>
        <a href='{$taxonomic_group}_{$protein_family}_results.zip' class='button download-results'> Download Results</a></div>";
    } else {
        echo "<p class='error'>Error: The results file is not available yet.</p>";
    }
}


	$aligned_seqs = "{$taxonomic_group}_{$protein_family}_alignment.fasta";
	//if (file_exists($aligned_seqs)){
	//	 echo("Found $aligned_seqs");	
	//}
	$prosite_tsv = "{$taxonomic_group}_{$protein_family}_motifs.tsv";
	//if (file_exists($prosite_tsv)) {
	//	echo "Found tsv file";
	//} else {
    	//	echo "File not found: $prosite_tsv";
	//}

	$prosite_csv = "{$taxonomic_group}_{$protein_family}_motifs.csv";
        //if (file_exists($prosite_csv)) {
	//	echo "Found $prosite_csv";	
	//} else {
	//	echo "File not found: $prosite_csv";
	//}
}

//Part 3: Sending information to MySQL
require_once 'login_credentials.php';

//3.c Creating a PDO instance
try{
	$pdo = new PDO("mysql:host=$server;dbname=$database;charset=utf8mb4",$username,$password, 
		[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    		PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
} catch (PDOException $e) {
	echo "Database connection failed";
}

//3.d Creating MySQL tables
if($pdo !== null && isset($PDreport) && $PDreport == 1) {
	try{
		$stmt = $pdo->query("SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'motifs'");
		$tableExists = ($stmt->rowCount() > 0);
		if($tableExists) {
			$pdo -> exec("DROP TABLE motifs");
		}
		motifs_table_maker($pdo);
		$stmt = $pdo -> prepare("INSERT INTO motifs (SeqName, Start, End, Score, Strand, Motif) VALUES (?, ?, ?, ?, ?, ?)");
		if (file_exists($prosite_csv) && ($csv_to_upload = fopen($prosite_csv, 'r')) !== false) {
			while (($row = fgetcsv($csv_to_upload, 0, ",")) !== false) {
				if (empty($row) || strpos($row[0], '#') === 0) continue;
				if (count($row) < 6) {
					error_log("Skipping incomplete row: " . implode(",", $row));
					continue;
				}	

				$stmt -> execute([
				$row[0],
				(int)$row[1],
				(int)$row[2],
				(float)$row[3],
				$row[4],
				$row[5]
				]);
			}
			fclose($csv_to_upload);
			//echo "Motifs imported successfully";
			echo "<html><body>";
            		echo "<table border='1'>";

            		// Display data from motifs table
            		$displaystmt = $pdo->query("SELECT * FROM motifs");
            		$results = $displaystmt->fetchAll(PDO::FETCH_ASSOC);

            		if (!empty($results)) {
				// Table headers
				echo "<table>";
				echo "<p>Given your particular interest in motif annotation, here lies a table with the fruits of your exploration</p>";
				echo "<caption>Motif Annotation Results</caption>";
				echo "<tr class='search-meta'><td colspan='100%'>Search: <strong>'$protein_family $taxonomic_group'</strong></td></tr>";
				//echo "<thead> $protein_family . $taxonomic_group</thead>";
				echo "<tr>";
                		foreach (array_keys($results[0]) as $columnName) {
                    			echo "<th>" . htmlspecialchars($columnName) . "</th>";
				}
				echo "</tr>";
				// Table data
                		foreach ($results as $row) {
                    			echo "<tr>";
                    			foreach ($row as $value) {
                        			echo "<td>" . htmlspecialchars($value) . "</td>";
					}
					echo "</tr>";
				}
				echo "</table>";
				} else { 
					echo "<table><tr><td colspan='6'>No motifs data found</td></tr>";
			}
			echo "</table>";
		} else {
			throw new Exception("Could not open $prosite_csv");
		} 
	} catch (PDOException $e) {
		echo "Database error: " . $e->getMessage();
		error_log("DB Error: " . $e->getMessage());
	} catch (Exception $e) {
		echo "Error: " . $e->getMessage();
	} 	
} else {
	echo "Prosite analysis not selected or database unavailable.";
}

echo	"</body>";
echo "</html>";

?>
