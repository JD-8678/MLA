<!DOCTYPE php>

<html lang="en">

	<head>
		<link rel="stylesheet" href="style.css" type="text/css">
		<title>Check your news</title>
	</head>
	<body>
		<div id="wrapper">
			<header>
				<h1>Das ist die Kopfzeile</h1>
			</header>
			<section>
				<form action="http://letkemann.ddns.net:9200" method="get">
					<input type="submit" value="Submit">
					<input type="submit" formmethod="post" value="Submit using POST">
				</form>

			</section>
			<aside>
				<input type="text" id="search_claims" name="search_claims" value="search">
				<button type="button" onclick="table_claims()">submit</button>
				<table id="claims">
					<tr>
						<th>link</th>
						<th>text</th>
					</tr>
				</table>

			</aside>
			<footer>Das ist die Fusszeile</footer>
		</div>



	</body>
</html>

