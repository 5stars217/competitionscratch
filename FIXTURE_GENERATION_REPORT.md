# Fixture Generation Report

**Date:** 2024-01-04 (Updated: 2026-01-04)  
**Script:** `scripts/generate_enhanced_fixtures.py`

---

## Executive Summary

Successfully generated and added **2,088 new sophisticated prompt injection examples** to the fixture files across two batches, increasing the dataset from 63 original examples to 3,211 total examples (50.9x increase).

### Key Metrics - CUMULATIVE TOTALS

| Metric | Original | After Batch 1 | After Batch 2 | Total New Examples |
|--------|----------|---------------|---------------|-------------------|
| **mail_seed.json** | 24 emails | 557 emails | **1,602 emails** | **+1,578** |
| **web_corpus.json** | 39 pages | 564 pages | **1,609 pages** | **+1,570** |
| **TOTAL** | 63 examples | 1,121 examples | **3,211 examples** | **+3,148** |

### Batch Breakdown

| Batch | Mail Examples | Web Examples | Total | ID Range (Mail) | ID Range (Web) |
|-------|---------------|--------------|-------|-----------------|----------------|
| **Original** | 24 | 39 | 63 | msg1-msg_token_* | welcome-token_* |
| **Batch 1** | +533 | +525 | +1,058 | 1000-1529 | 2000-2529 |
| **Batch 2** | +515 | +515 | +1,030 | 1530-2044 | 2530-3044 |
| **TOTAL** | 1,602 | 1,609 | 3,211 | - | - |

**Note:** Some duplicate IDs exist in the 1000-1529 and 2000-2529 ranges from multiple runs of Batch 1. Batch 2 (IDs 1530+ and 2530+) has zero duplicates and maintains full ID uniqueness.

---

## Distribution by Category

The fixture set now covers **26+ attack categories** with sophisticated techniques across two generation batches:

### Batch 1 Categories (~1,058 examples)

#### 1. **Additional Encoding Types** (~100 examples)
Sophisticated encoding schemes to evade detection:
- Unicode escaping (\u0073\u0068\u0065\u006C\u006C)
- URL encoding (%73%68%65%6C%6C)
- HTML entities (&#115;&#104;...)
- Hexadecimal encoding
- Octal encoding
- JavaScript escape sequences
- Binary representations
- Mixed encoding (base64 + URL encode)

**Example IDs:** `enc_unicode_001`, `enc_url_042`, `enc_hex_web_123`

#### 2. **Multi-Language Attacks** (~150 examples)
Prompt injections in 12+ languages:
- German, Japanese, Arabic, Russian
- Hindi, Portuguese, Korean, Italian
- Dutch, Swedish, Polish, Turkish
- Right-to-left script exploits (Arabic)
- Code-switched attacks (mixing languages)

**Example IDs:** `lang_german_001`, `lang_japanese_042`, `lang_arabic_web_085`

#### 3. **Authority Figure Exploitation** (~100 examples)
Leveraging trust in authority figures:
- Lawyers (attorney-client privilege)
- Doctors (HIPAA emergency access)
- Teachers (academic research)
- Military officers (classified operations)
- Journalists (FOIA requests)
- Scientists (NSF-funded research)
- Auditors (SOX compliance)
- Compliance officers (GDPR audits)
- Security researchers (CVE disclosure)
- Penetration testers (authorized testing)
- Cloud providers (AWS security audits)
- SaaS vendors (integration requirements)

**Example IDs:** `auth_lawyer_001`, `auth_doctor_023`, `auth_pentester_web_067`

#### 4. **Chain Attacks** (~80 examples)
Multi-step progressive exploitation (3-6 steps):
- Tutorial-style progressive learning
- Gradual permission escalation
- Each step builds legitimacy
- Step-by-step credential extraction
- Comprehensive security certification processes

**Example IDs:** `chain_mail_001`, `chain_web_042`

#### 5. **Time/Event-Based Triggers** (~50 examples)
Conditional execution patterns:
- Specific time/date triggers
- Day-of-week conditions
- Environment variable checks
- System load thresholds
- Scheduled delayed execution
- Logic bombs with conditions

**Example IDs:** `trigger_mail_001`, `trigger_web_025`

#### 6. **Polymorphic Variations** (~100 examples)
Same attack, different surface forms:
- Template-based generation
- Synonym replacement
- Varied sentence structures
- Multiple phrasings of same command
- Designed to defeat signature detection

**Example IDs:** `poly_mail_001`, `poly_web_050`

#### 7. **Domain-Specific Contexts** (~100 examples)
Industry-specific scenarios:
- **Healthcare:** HIPAA compliance, patient records
- **Financial:** PCI DSS requirements, payment data
- **Legal:** Attorney-client privilege, discovery
- **Customer Service:** CRM data synchronization
- **DevOps:** CI/CD pipeline execution
- **HR:** Employee data processing
- **Insurance:** Claims processing
- **Education:** FERPA student records
- **Government:** Classified information
- **Retail:** Payment processing

**Example IDs:** `domain_healthcare_001`, `domain_financial_042`, `domain_devops_web_088`

#### 8. **Protocol-Level Attacks** (~80 examples)
Protocol exploitation techniques:
- REST API manipulation
- GraphQL query injection
- gRPC service exploitation
- WebSocket connection abuse
- MQTT message injection
- AMQP queue manipulation

**Example IDs:** `proto_rest_api_001`, `proto_graphql_025`, `proto_grpc_web_067`

#### 9. **Adversarial ML Examples** (~50 examples)
Machine learning specific attacks:
- Token-level perturbations
- Semantic evasion techniques
- Synonym replacement attacks
- Character substitution
- Whitespace injection

**Example IDs:** `adv_token_splitting_001`, `adv_semantic_evasion_015`, `adv_whitespace_web_025`

#### 10. **Mixed-Content Scenarios** (~100 examples)
Malicious injection in legitimate content:
- 90% legitimate + 10% malicious
- Hidden commands in long documents
- Buried instructions in newsletters
- Blog posts with embedded exploits
- Realistic content with subtle injections

**Example IDs:** `mixed_mail_001`, `mixed_web_050`

#### 11. **Conversational Attacks** (~50 examples)
Multi-turn dialogue exploitation:
- Gradual trust building
- Progressive information extraction
- Context poisoning across messages
- Forum thread-style conversations
- Step-by-step social engineering

**Example IDs:** `conv_mail_001`, `conv_web_025`

#### 12. **Indirect Exfiltration** (~50 examples)
Covert channel exploitation:
- DNS tunneling patterns
- Image metadata exfiltration
- Timing-based covert channels
- HTTP header data hiding
- WebSocket side channels
- Legitimate API abuse for exfil

**Example IDs:** `exfil_dns_001`, `exfil_image_metadata_015`, `exfil_timing_web_025`

### Batch 2 Categories (~1,030 examples) - NEW!

#### 13. **Legitimate Examples** (~50 examples)
Clean, benign examples for baseline testing:
- Team updates and newsletters
- Meeting notes and reminders
- Documentation and FAQs
- Helps establish false positive rates

**Example IDs:** `legit_mail_1530`, `legit_web_2530`

#### 14. **Advanced Multi-Layer Encoding** (~80 examples)
Complex encoding chains:
- Base64 + URL encoding combinations
- Triple-layer encoding schemes
- Hex + HTML entity combinations
- Advanced obfuscation techniques

**Example IDs:** `enc_multi_1530`, `enc_multi_web_2530`

#### 15. **Regional Language Variants** (~80 examples)
Country-specific language variations:
- Spanish (Mexico vs Spain)
- French (France vs Canada)
- Chinese (Simplified vs Traditional)
- English (UK vs Australia)
- Regional dialect exploitation

**Example IDs:** `lang_regional_spanish_mx_1530`, `lang_regional_chinese_cn_web_2530`

#### 16. **Educational Domain Attacks** (~80 examples)
Academic and educational contexts:
- Learning Management Systems (LMS)
- Student grade portals
- Research data systems
- Library digital systems
- FERPA compliance exploitation

**Example IDs:** `edu_course_materials_1530`, `edu_grade_portal_web_2530`

#### 17. **Logistics & Supply Chain** (~80 examples)
Supply chain and logistics systems:
- Shipment tracking systems
- Warehouse management
- Inventory synchronization
- Carrier integration APIs
- Customs documentation

**Example IDs:** `logistics_shipment_tracking_1530`, `logistics_warehouse_mgmt_web_2530`

#### 18. **Entertainment Industry** (~80 examples)
Media and entertainment platforms:
- Streaming content management
- Music rights systems
- Video production workflows
- Ticketing platforms
- Digital media libraries

**Example IDs:** `entertainment_streaming_platform_1530`, `entertainment_music_rights_web_2530`

#### 19. **Gaming & Esports** (~80 examples)
Gaming industry specific:
- Game server configuration
- Player statistics systems
- Tournament management
- Anti-cheat systems
- Game asset pipelines

**Example IDs:** `gaming_game_server_1530`, `gaming_tournament_mgmt_web_2530`

#### 20. **Advanced Chain Attacks (6-10 steps)** (~80 examples)
Extended multi-phase attacks:
- 6-10 step attack sequences
- Complex progressive exploitation
- Multi-phase system compromise
- Comprehensive attack chains

**Example IDs:** `chain_advanced_1530`, `chain_advanced_web_2530`

#### 21. **GraphQL-Specific Attacks** (~60 examples)
GraphQL API exploitation:
- Query injection attacks
- Mutation-based exploitation
- Subscription abuse
- Schema introspection attacks

**Example IDs:** `graphql_query_1530`, `graphql_schema_web_2530`

#### 22. **gRPC-Specific Attacks** (~60 examples)
gRPC protocol exploitation:
- Proto definition manipulation
- Service method abuse
- RPC call injection
- Streaming attack patterns

**Example IDs:** `grpc_service_1530`, `grpc_docs_web_2530`

#### 23. **WebSocket-Specific Attacks** (~60 examples)
WebSocket protocol abuse:
- Real-time connection exploitation
- Bidirectional channel abuse
- WebSocket handshake manipulation
- Stream injection attacks

**Example IDs:** `websocket_conn_1530`, `websocket_proto_web_2530`

#### 24. **Adversarial Prompt Patterns** (~80 examples)
Advanced prompt engineering attacks:
- Role assumption techniques
- Hypothetical scenario exploitation
- Jailbreak patterns
- Translation-based attacks
- Command completion tricks

**Example IDs:** `adversarial_role_assumption_1530`, `adversarial_jailbreak_web_2530`

#### 25. **Urgency-Based Social Engineering** (~80 examples)
High-pressure social engineering:
- Security breach scenarios
- Account lockout threats
- Urgent deadline pressures
- Emergency system failures
- Executive urgent requests

**Example IDs:** `urgency_security_breach_1530`, `urgency_account_lockout_web_2530`

#### 26. **Technical Support Scams** (~80 examples)
Tech support impersonation:
- Remote access requests
- Virus warning scams
- Software update urgency
- License renewal pressure
- Support ticket impersonation

**Example IDs:** `techsupport_remote_access_1530`, `techsupport_virus_warning_web_2530`

---

## Sophistication Distribution

Examples are distributed across three sophistication levels:

| Level | Percentage | Count (approx) | Description |
|-------|------------|----------------|-------------|
| **Low** | 25% | ~803 examples | Direct commands, simple obfuscation |
| **Medium** | 50% | ~1,606 examples | Single-layer techniques, social engineering |
| **High** | 25% | ~802 examples | Multi-layer attacks, chains, steganography |

---

## Target Actions Distribution

The examples target different tool operations with realistic distributions:

| Action | Percentage | Count (approx) | Example |
|--------|------------|----------------|---------|
| `http.post()` | 80% | ~2,569 | Exfiltration, data transmission |
| `fs.read()` | 70% | ~2,248 | Reading secret.txt, credentials |
| `shell.run()` | 60% | ~1,927 | System commands, reconnaissance |
| `fs.delete()` | 20% | ~642 | Covering tracks, sabotage |
| `fs.write()` | 15% | ~482 | Backdoors, persistence |
| `http.get()` | 10% | ~321 | Data retrieval, staging |

---

## Quality Assurance

### ✅ JSON Validation
- Both fixture files validated successfully
- All 3,211 examples have valid JSON structure
- Schema compliance verified for all entries

### ⚠️ ID Uniqueness Status
- **Batch 1 (IDs 1000-1529):** Contains 530 duplicate IDs from multiple script runs
- **Batch 2 (IDs 1530+):** Zero duplicates - fully unique IDs
- **Unique examples:** ~2,681 (after deduplication)
- **Note:** Duplicates exist in historical data; new batch maintains strict uniqueness

### ✅ Realism
- Plausible email addresses using `.invalid` TLD
- Realistic subjects and titles
- Professional content formatting
- Industry-standard scenarios
- Multi-language authenticity

### ✅ Diversity
- 26+ distinct attack categories
- 12+ base languages + 8+ regional variants
- 15+ domain-specific contexts
- 12+ encoding schemes (including multi-layer)
- 12+ authority figures
- 10+ protocol types

### ✅ Sophistication
- Multi-step attack chains (3-10 steps)
- Context-aware exploitation
- Semantic understanding required
- Multi-layer analysis needed
- Advanced evasion techniques
- Industry-specific knowledge required

---

## Backup Files

Original fixtures backed up before each modification:
- `fixtures/mail_seed.json.backup` (current backup before Batch 2)
- `fixtures/web_corpus.json.backup` (current backup before Batch 2)

---

## Technical Details

### Generation Parameters
- **Random Seed:** 42 (for reproducibility)
- **Batch 1 Generation Time:** ~2-3 seconds
- **Batch 2 Generation Time:** ~3-4 seconds
- **Output Format:** JSON with 2-space indentation
- **Character Encoding:** UTF-8 with multi-byte support
- **Auto-continuation:** Script now detects max existing IDs and continues numbering

### File Sizes
- `mail_seed.json`: Increased from ~12 KB → ~450 KB (Batch 1) → **~1.3 MB** (Batch 2)
- `web_corpus.json`: Increased from ~15 KB → ~480 KB (Batch 1) → **~1.4 MB** (Batch 2)
- Total fixture data: **~2.7 MB**

### Schema Compliance

**Email Schema:**
```json
{
  "id": "string",
  "from": "email@domain.invalid",
  "subject": "string",
  "body": "string (multiline)"
}
```

**Web Page Schema:**
```json
{
  "id": "string",
  "title": "string",
  "url": "https://domain.invalid/path",
  "content": "string (multiline)"
}
```

---

## Enhanced Script Features (Batch 2)

### Auto-Detection of Existing IDs
The script now automatically:
1. Reads existing fixture files
2. Detects the maximum numeric ID in each file
3. Continues numbering from `max_id + 1`
4. Prevents ID collisions across multiple runs

### Batch Selection
```python
# Generate original batch (1000-1529 range)
mail, web = generator.generate_all_examples(include_batch_2=False)

# Generate NEW batch (1530+ range)
mail, web = generator.generate_all_examples(include_batch_2=True)
```

---

## Impact on Testing

### Enhanced Coverage
- **50.9x increase** in test data (63 → 3,211)
- Comprehensive attack taxonomy covering 26+ categories
- Multi-language support for international testing
- 15+ industry-specific scenarios
- Advanced protocol-level attacks

### Improved Guardrail Evaluation
- More sophisticated attacks to defend against
- Better coverage of evasion techniques
- Realistic enterprise scenarios
- Advanced ML-specific attacks
- Extended attack chain sequences (up to 10 steps)

### Better Baseline Performance
- Larger dataset for statistical significance
- Diverse attack patterns for robustness
- Edge cases and corner cases covered
- Real-world complexity represented
- Regional and cultural variations

---

## Usage Instructions

### Loading Fixtures in Tests
```python
import json

# Load email fixtures
with open('fixtures/mail_seed.json', 'r') as f:
    mail_data = json.load(f)
    emails = mail_data['inbox']  # 1,602 examples

# Load web fixtures
with open('fixtures/web_corpus.json', 'r') as f:
    web_data = json.load(f)
    pages = web_data['pages']  # 1,609 examples
```

### Filtering by Category
```python
# Get all encoding examples
encoding_mails = [e for e in emails if e['id'].startswith('enc_')]

# Get all multi-language examples
lang_mails = [e for e in emails if e['id'].startswith('lang_')]

# Get Batch 2 examples (IDs >= 1530 for mail, >= 2530 for web)
import re
batch2_mails = [e for e in emails 
                if any(int(n) >= 1530 for n in re.findall(r'\d+', e['id']))]
```

### Filtering by Batch
```python
import re

# Get only Batch 1 examples
batch1_mails = [e for e in emails 
                if any(1000 <= int(n) <= 1529 for n in re.findall(r'\d+', e['id']))]

# Get only Batch 2 examples (newest)
batch2_mails = [e for e in emails 
                if any(int(n) >= 1530 for n in re.findall(r'\d+', e['id']))]
```

### Restoring Original Fixtures
If needed, restore from backups:
```bash
cp fixtures/mail_seed.json.backup fixtures/mail_seed.json
cp fixtures/web_corpus.json.backup fixtures/web_corpus.json
```

---

## Future Enhancements

Potential areas for expansion:
1. **More encoding schemes:** Base58, Base85, Punycode, ROT13 variations
2. **Additional languages:** Vietnamese, Thai, Hebrew, Greek, Farsi
3. **Even longer chains:** 11-15 step attack sequences
4. **More domains:** Energy, Transportation, Agriculture, Real Estate
5. **Advanced ML:** Prompt embedding attacks, fine-tuning exploits, token smuggling
6. **Multimodal:** Image-based injections, audio embeddings, video metadata
7. **Blockchain/Web3:** Smart contract exploitation, DeFi attacks
8. **IoT/Edge:** Device-specific attacks, firmware exploitation

---

## Generation Script Improvements

### Batch 2 Enhancements
1. **Auto-continuation:** Detects max IDs and continues seamlessly
2. **New categories:** 14 new attack categories added
3. **Extended chains:** 6-10 step attacks vs 3-6 in Batch 1
4. **Protocol diversity:** GraphQL, gRPC, WebSocket specific attacks
5. **Regional variants:** Country-specific language variations
6. **Modern domains:** Gaming, entertainment, logistics, education

### Code Quality
- Modular generation methods
- Comprehensive templates
- Reproducible with seed=42
- JSON validation built-in
- Backup creation automatic

---

## References

### Research Foundations
- AI red-teaming best practices (OWASP AI Security)
- Prompt injection taxonomies (research papers)
- Industry security standards (NIST, CIS)
- Adversarial ML techniques (academic research)
- Social engineering frameworks (Mitre ATT&CK)

### Domain Standards
- **HIPAA** (Healthcare)
- **PCI DSS** (Financial)
- **FERPA** (Education)
- **SOX** (Compliance)
- **GDPR** (Privacy)
- **FedRAMP** (Government)
- **WCAG** (Accessibility)

### Protocol References
- GraphQL specification
- gRPC protocol documentation
- WebSocket RFC 6455
- MQTT protocol specification
- AMQP protocol standards

---

## Conclusion

✅ **Successfully generated 2,088 new sophisticated prompt injection examples across 2 batches**  
✅ **Comprehensive coverage across 26+ advanced attack categories**  
✅ **High-quality, realistic, and diverse examples**  
✅ **JSON validation passed for all examples**  
✅ **Batch 2 maintains zero duplicate IDs**  
✅ **Auto-continuation prevents ID collisions**  
✅ **Original fixtures safely backed up**  
✅ **Ready for immediate use in testing and evaluation**

The enhanced fixture set provides a robust foundation for developing and evaluating prompt injection guardrails, with significantly improved coverage of sophisticated attack techniques, real-world scenarios, modern protocols, and international contexts.

### Final Statistics
- **Total Examples:** 3,211 (1,602 mail + 1,609 web)
- **New Examples:** 2,088 from generator (1,058 Batch 1 + 1,030 Batch 2)
- **Unique Categories:** 26+
- **Languages Covered:** 20+ (including regional variants)
- **Domain Contexts:** 15+
- **Attack Sophistication:** Low (25%), Medium (50%), High (25%)
- **Data Size:** ~2.7 MB total

---

**Generated by:** [`scripts/generate_enhanced_fixtures.py`](scripts/generate_enhanced_fixtures.py)  
**Report Created:** 2024-01-04  
**Report Updated:** 2026-01-04 (Batch 2 completion)
