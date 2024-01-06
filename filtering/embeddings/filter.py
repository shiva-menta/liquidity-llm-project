import os
import re
keywords = [
    'liquidity (event|crisis|problems?|issues?|shortage)', 'bank run', 'banking panic',
    'bank failure', 'financial contagion', 'cash crunch', 'money squeeze',
    'asset (liquidation|sales?|sell-off)', 'credit (crunch|freeze|squeeze)',
    'financial emergency', 'loan crisis', 'debt crisis', 'funding gap',
    'central bank (intervention|bailout|support)', 'overleverag(e|ing)', 'withdrawals?', 'withdraw', 'withdrew',
    'depositor (confidence|withdrawals?|run)', 'cash flow (problems?|crisis|shortfall)',
    'borrowing (difficulties|challenges)', 'credit line', 'credit access',
    'IPO', 'M&A', 'VC exit', 'PE exit', 'divestiture', 'solvency crisis',
    'financial obligations', 'short-term (obligations|funding)', 'emergency (loan|funding)',
    'interbank (lending|borrowing|market)', 'fire sale', 'economic (downturn|collapse)',
    'market (crash|turmoil)', 'financial (instability|distress)', 'panic (withdrawal|selling)',
    'insolvency', 'bankruptcy', 'bailout', 'federal reserve', 'ECB', 'systemic risk',
    'market volatility', 'stock market crash', 'investment risk', 'bubble burst',
    'financial meltdown', 'toxic assets', 'bad debts', 'non-performing (loans|assets)',
    'risk management failure', 'regulatory failure', 'policy response',
    'government intervention', 'economic rescue', 'fiscal stimulus',
    'quantitative easing', 'interest rate (hike|cut)', 'financial regulation',
    'economic bailout', 'debt burden', 'credit default', 'loan default',
    'leverage ratio', 'capital adequacy', 'bank distress', 'financial shock',
    'market sentiment', 'investor confidence', 'economic uncertainty',
    'financial stability', 'banking sector (woes|trouble)', 'lender of last resort'
]
directory = './files/combined_json_files'
output_directory = './files/filtered_json_files_2'
pattern = re.compile('|'.join(keywords), re.IGNORECASE)
# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        output_data = []
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    # Find the 'body' field in the JSON line
                    body_header = line.find('"body": "')
                    if body_header != -1:
                        # Extract the content of the 'body' field
                        body_text_start = body_header + 9
                        body_text_end = line.find('"', body_text_start)
                        body_text = line[body_text_start:body_text_end]
                        # Check if the body text matches the pattern
                        match = pattern.search(body_text)
                        if match:
                            # Find the last closing brace
                            last_brace = line.rfind('}')
                            if last_brace != -1:
                                # Insert the matched keyword before the last brace
                                matched_keyword = f', "matched_keyword": "{match.group()}"'
                                new_line = line[:last_brace] + matched_keyword + line[last_brace:]
                                output_data.append(new_line.strip())
                except Exception as e:
                    print(f"Error processing line in file {filename}: {e}")
        # Write filtered data to a new file in the output directory
        if output_data:
            with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as outfile:
                for item in output_data:
                    outfile.write(item + '\n')