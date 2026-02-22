let sessionId = null;
let selectedFile = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeThreatMeter();
    loadThreatIntelligence();
    initializeAttackSimulator(); // NEW
});

// Tab Navigation
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));

            tab.classList.add('active');
            const targetContent = document.getElementById(`${targetTab}-tab`);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            if (targetTab === 'intel') {
                loadThreatIntelligence();
            } else if (targetTab === 'dashboard') {
                loadDashboard();
            }
        });
    });
}

// Initialize Attack Simulator
function initializeAttackSimulator() {
    console.log("Initializing attack simulator...");

    const attackRSABtn = document.getElementById('attackRSA');
    const attackKyberBtn = document.getElementById('attackKyber');
    const attackBothBtn = document.getElementById('attackBoth');

    if (attackRSABtn) {
        attackRSABtn.addEventListener('click', () => {
            console.log("Attack RSA clicked");
            simulateAttack('rsa', 2048);
        });
    }

    if (attackKyberBtn) {
        attackKyberBtn.addEventListener('click', () => {
            console.log("Attack Kyber clicked");
            simulateAttack('kyber', 768);
        });
    }

    if (attackBothBtn) {
        attackBothBtn.addEventListener('click', async () => {
            console.log("Attack both clicked");
            await simulateAttack('rsa', 2048);
            await new Promise(resolve => setTimeout(resolve, 2000));
            await simulateAttack('kyber', 768);
        });
    }
}

// Attack Simulator Functions
async function simulateAttack(algorithm, keySize) {
    console.log(`Simulating attack on ${algorithm}-${keySize}`);

    const vizDiv = document.getElementById('attackVisualization');
    const resultsDiv = document.getElementById('attackResults');
    const progressBar = document.getElementById('attackProgress');
    const stageTitle = document.querySelector('.stage-title');
    const stageMessage = document.getElementById('attackMessage');

    if (!vizDiv || !resultsDiv || !progressBar || !stageTitle || !stageMessage) {
        console.error("Attack visualization elements not found!");
        return;
    }

    vizDiv.style.display = 'block';
    resultsDiv.classList.add('hidden');
    resultsDiv.innerHTML = '';
    progressBar.style.width = '0%';

    try {
        const response = await fetch('/api/simulate-attack', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm, key_size: keySize })
        });

        const data = await response.json();

        if (data.success) {
            // Animate through stages
            for (const stage of data.stages) {
                stageTitle.textContent = stage.message;
                stageMessage.textContent = `Stage: ${stage.stage.replace(/_/g, ' ').toUpperCase()}`;
                progressBar.style.width = stage.progress + '%';

                // Change color based on vulnerability
                if (stage.vulnerable) {
                    progressBar.style.background = 'linear-gradient(90deg, #f87171, #fbbf24)';
                } else {
                    progressBar.style.background = 'linear-gradient(90deg, #60a5fa, #34d399)';
                }

                await new Promise(resolve => setTimeout(resolve, stage.time * 1000));
            }

            // Show final result
            showAttackResult(data);
        } else {
            console.error("Attack simulation failed:", data.error);
            alert("Attack simulation failed: " + data.error);
        }
    } catch (error) {
        console.error('Attack simulation error:', error);
        alert("Error running attack simulation. Check console for details.");
    }
}

function showAttackResult(data) {
    const resultsDiv = document.getElementById('attackResults');
    const lastStage = data.stages[data.stages.length - 1];

    const resultClass = lastStage.broken ? 'result-broken' : 'result-secure';
    const resultIcon = lastStage.broken ? '🚨💀' : '✅🛡️';
    const resultText = lastStage.broken ?
        `<strong style="font-size: 1.5rem; color: #f87171;">ENCRYPTION BROKEN!</strong><br><br>
        <strong>Algorithm:</strong> ${data.algorithm.toUpperCase()}-${lastStage.broken ? '2048' : '768'}<br>
        <strong>Simulation Time:</strong> ${data.total_time.toFixed(1)} seconds<br>
        <strong>Real-World Equivalent:</strong> ~8.3 hours with 4096-qubit quantum computer<br>
        <strong>Status:</strong> <span style="color: #f87171;">⚠️ VULNERABLE TO QUANTUM ATTACKS</span><br><br>
        <em>This demonstrates why RSA must be replaced with quantum-safe algorithms like Kyber.</em>` :
        `<strong style="font-size: 1.5rem; color: #34d399;">ENCRYPTION SECURE!</strong><br><br>
        <strong>Algorithm:</strong> ${data.algorithm.toUpperCase()}-768<br>
        <strong>Simulation Time:</strong> ${data.total_time.toFixed(1)} seconds<br>
        <strong>Real-World Equivalent:</strong> 10,000+ years (computationally infeasible)<br>
        <strong>Status:</strong> <span style="color: #34d399;">✅ QUANTUM-RESISTANT</span><br><br>
        <em>Kyber-768 remains secure even against quantum computers due to lattice-based mathematics.</em>`;

    resultsDiv.innerHTML = `
        <div class="attack-result ${resultClass}">
            <div class="result-icon">${resultIcon}</div>
            <div style="font-size: 1.1rem; line-height: 2; text-align: left;">
                ${resultText}
            </div>
        </div>
    `;

    resultsDiv.classList.remove('hidden');
}

// Threat Meter
function initializeThreatMeter() {
    fetch('/api/threat-intel')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const prediction = data.rsa2048_prediction;
                const yearsRemaining = prediction.years_remaining;
                const threatLevel = prediction.threat_level;

                const maxYears = 15;
                const fillPercent = Math.min(100, ((maxYears - yearsRemaining) / maxYears) * 100);

                document.getElementById('threatFill').style.width = fillPercent + '%';
                document.getElementById('threatText').textContent =
                    `${threatLevel} - RSA-2048 will be broken in ${yearsRemaining} years (${prediction.predicted_breaking_year})`;
            }
        })
        .catch(err => {
            document.getElementById('threatText').textContent = 'Error loading threat data';
        });
}

// Generate Keys
document.getElementById('generateKeys').addEventListener('click', async () => {
    const algorithm = document.querySelector('input[name="algorithm"]:checked').value;
    const statusDiv = document.getElementById('keyStatus');
    const btn = document.getElementById('generateKeys');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    statusDiv.className = 'status-message';
    statusDiv.style.display = 'none';

    try {
        const response = await fetch('/api/generate-keys', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm })
        });

        const data = await response.json();

        if (data.success) {
            sessionId = data.session_id;
            statusDiv.className = 'status-message success';
            statusDiv.innerHTML = `
                ✅ Keys generated successfully!<br>
                Algorithm: ${algorithm.toUpperCase()}<br>
                Time: ${(data.generation_time * 1000).toFixed(3)}ms
            `;
            document.getElementById('encryptBtn').disabled = false;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        statusDiv.className = 'status-message error';
        statusDiv.textContent = `❌ Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-key"></i> Generate Encryption Keys';
    }
});

// File Selection
document.getElementById('fileInput').addEventListener('change', (e) => {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        document.getElementById('fileName').textContent =
            `✓ Selected: ${selectedFile.name} (${(selectedFile.size / 1024).toFixed(2)} KB)`;
    }
});

// Encrypt File
document.getElementById('encryptBtn').addEventListener('click', async () => {
    if (!selectedFile || !sessionId) return;

    const statusDiv = document.getElementById('encryptStatus');
    const aiAnalysisDiv = document.getElementById('aiAnalysis');
    const btn = document.getElementById('encryptBtn');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Encrypting...';
    statusDiv.className = 'status-message';
    statusDiv.style.display = 'none';
    aiAnalysisDiv.classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('session_id', sessionId);

        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            const meta = data.metadata;
            const ai = data.ai_analysis;

            // Build download URL and inject button
            const downloadUrl = `/api/download-encrypted?session_id=${encodeURIComponent(sessionId)}`;
            const keyDownloadUrl = `/api/export-keys?session_id=${encodeURIComponent(sessionId)}`;

            statusDiv.style.display = '';  // clear inline style so CSS class can show it
            statusDiv.className = 'status-message success';
            statusDiv.innerHTML = `
                ✅ File encrypted successfully!<br>
                Algorithm: ${meta.algorithm.toUpperCase()}<br>
                Encryption Time: ${(meta.encryption_time * 1000).toFixed(3)}ms<br>
                Original Size: ${(meta.original_size / 1024).toFixed(2)} KB<br><br>
                <a href="${downloadUrl}" download
                   style="display:inline-block; margin-top:8px; padding:12px 28px;
                          background: linear-gradient(135deg,#34d399,#059669);
                          color:#fff; font-weight:700; border-radius:10px;
                          text-decoration:none; font-size:1rem;
                          box-shadow:0 4px 15px rgba(52,211,153,0.4);
                          transition: transform 0.2s, box-shadow 0.2s;"
                   onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 20px rgba(52,211,153,0.6)'"
                   onmouseout="this.style.transform='';this.style.boxShadow='0 4px 15px rgba(52,211,153,0.4)'">
                   ⬇️ Download Encrypted File
                </a>
                &nbsp;&nbsp;
                <a href="${keyDownloadUrl}" download="qbits_private_key.json"
                   style="display:inline-block; margin-top:8px; padding:12px 28px;
                          background: linear-gradient(135deg,#f59e0b,#d97706);
                          color:#fff; font-weight:700; border-radius:10px;
                          text-decoration:none; font-size:1rem;
                          box-shadow:0 4px 15px rgba(245,158,11,0.4);
                          transition: transform 0.2s, box-shadow 0.2s;"
                   onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 20px rgba(245,158,11,0.6)'"
                   onmouseout="this.style.transform='';this.style.boxShadow='0 4px 15px rgba(245,158,11,0.4)'">
                   🔑 Download Key File
                </a>
                <br><small style="opacity:0.7; font-size:0.75rem;">💡 Save the Key File — you'll need it to decrypt this file in future sessions</small>
            `;



            if (ai) {
                const statusIcon = ai.is_anomaly ? '🔴' : '🟢';

                aiAnalysisDiv.classList.remove('hidden');
                aiAnalysisDiv.innerHTML = `
                    <h3>${statusIcon} AI Security Analysis</h3>
                    <p><strong>Status:</strong> ${ai.is_anomaly ? 'Anomaly Detected' : 'Normal Operation'}</p>
                    <p><strong>Risk Level:</strong> <span style="color: ${getRiskColor(ai.risk_level)}">${ai.risk_level}</span></p>
                    <p><strong>Confidence:</strong> ${ai.confidence.toFixed(1)}%</p>
                    ${ai.is_anomaly ? `
                        <div style="margin-top: 15px; padding: 15px; background: rgba(248, 113, 113, 0.1); border-left: 3px solid var(--danger); border-radius: 8px;">
                            <strong>⚠️ Recommendations:</strong>
                            ${ai.recommendations.map(rec => `<br>• ${rec}`).join('')}
                        </div>
                    ` : ''}
                `;
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        statusDiv.style.display = '';  // clear inline style
        statusDiv.className = 'status-message error';
        statusDiv.textContent = `❌ Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-lock"></i> Encrypt File';
    }
});

function getRiskColor(level) {
    const colors = {
        'CRITICAL': '#f87171',
        'HIGH': '#fb923c',
        'MEDIUM': '#fbbf24',
        'LOW': '#34d399'
    };
    return colors[level] || '#60a5fa';
}

// Benchmark
document.getElementById('benchmarkBtn').addEventListener('click', async () => {
    const btn = document.getElementById('benchmarkBtn');
    const resultsDiv = document.getElementById('benchmarkResults');

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    resultsDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><span>Running 50 iterations...</span></div>';

    try {
        const response = await fetch('/api/benchmark', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ iterations: 50 })
        });

        const data = await response.json();

        if (data.success) {
            const kyber = data.kyber;
            const rsa = data.rsa;

            resultsDiv.innerHTML = `
                <div class="result-grid">
                    <div class="result-item">
                        <h4>Key Generation</h4>
                        <div class="value">${kyber.keygen.toFixed(3)}ms</div>
                        <small>Kyber (${(rsa.keygen / kyber.keygen).toFixed(0)}x faster)</small>
                    </div>
                    <div class="result-item">
                        <h4>Encryption</h4>
                        <div class="value">${kyber.encrypt.toFixed(3)}ms</div>
                        <small>Kyber (${(rsa.encrypt / kyber.encrypt).toFixed(0)}x faster)</small>
                    </div>
                    <div class="result-item">
                        <h4>Decryption</h4>
                        <div class="value">${kyber.decrypt.toFixed(3)}ms</div>
                        <small>Kyber (${(rsa.decrypt / kyber.decrypt).toFixed(0)}x faster)</small>
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 20px; background: rgba(52, 211, 153, 0.1); border: 1px solid var(--success); border-radius: 12px;">
                    <p style="color: var(--success); font-weight: 600; text-align: center;">
                        ✅ Kyber-768 is significantly faster while providing quantum resistance!
                    </p>
                </div>
            `;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        resultsDiv.innerHTML = `<p style="color: var(--danger)">❌ Error: ${error.message}</p>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play-circle"></i> Run Benchmark (50 iterations)';
    }
});

// Threat Intelligence
function loadThreatIntelligence() {
    const contentDiv = document.getElementById('threatIntelContent');

    fetch('/api/threat-intel')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const report = data.report;
                const predictions = report.predictions;

                let html = '<div class="result-grid">';

                for (const [algo, pred] of Object.entries(predictions)) {
                    const threatColor = getRiskColor(pred.threat_level);

                    html += `
                        <div class="result-item">
                            <h4>${algo}</h4>
                            <div class="value" style="color: ${threatColor}">${pred.predicted_breaking_year}</div>
                            <small>Breaks in ${pred.years_remaining} years</small>
                            <div style="margin-top: 10px; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                <div style="font-size: 0.8rem; color: var(--text-secondary);">Progress: ${pred.progress_percentage.toFixed(1)}%</div>
                                <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin-top: 5px; overflow: hidden;">
                                    <div style="height: 100%; background: ${threatColor}; width: ${pred.progress_percentage}%;"></div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                html += '</div>';

                html += `
                    <div style="margin-top: 30px; padding: 25px; background: var(--glass-bg); backdrop-filter: blur(10px); border: 1px solid var(--glass-border); border-radius: 16px;">
                        <h3 style="color: var(--primary); margin-bottom: 15px; font-family: 'Space Mono', monospace;">
                            <i class="fas fa-exclamation-triangle"></i> Overall Assessment
                        </h3>
                        <p style="color: var(--text-secondary); line-height: 1.8;">
                            <strong>Earliest Breaking Year:</strong> ${report.overall_assessment.earliest_breaking_year}<br>
                            <strong>Years Remaining:</strong> ${report.overall_assessment.years_remaining}<br>
                            <strong>Threat Level:</strong> <span style="color: ${getRiskColor(report.overall_assessment.threat_level)}">${report.overall_assessment.threat_level}</span><br><br>
                            <strong>Recommendation:</strong> ${report.overall_assessment.recommended_action}
                        </p>
                    </div>
                `;

                contentDiv.innerHTML = html;
            }
        })
        .catch(err => {
            contentDiv.innerHTML = '<p style="color: var(--danger)">Error loading threat intelligence</p>';
        });
}

// Risk Assessment
document.getElementById('assessRisk').addEventListener('click', async () => {
    const encryptionDate = document.getElementById('encryptionDate').value;
    const sensitivity = document.getElementById('sensitivity').value;
    const resultDiv = document.getElementById('riskResult');

    try {
        const response = await fetch('/api/assess-data-risk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                encryption_date: encryptionDate,
                sensitivity: sensitivity,
                algorithm: 'RSA-2048'
            })
        });

        const data = await response.json();

        if (data.success) {
            const risk = data.risk_assessment;
            const riskColor = getRiskColor(risk.risk_score > 70 ? 'HIGH' : risk.risk_score > 40 ? 'MEDIUM' : 'LOW');

            resultDiv.innerHTML = `
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="font-size: 4rem; font-weight: 700; color: ${riskColor}; font-family: 'Space Mono', monospace; text-shadow: 0 0 30px ${riskColor};">
                        ${risk.risk_score}
                    </div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary); margin-top: -10px;">RISK SCORE (out of 100)</div>
                </div>
                
                <div style="display: grid; gap: 15px;">
                    <div style="padding: 15px; background: var(--glass-bg); border-radius: 12px;">
                        <strong>📅 Encrypted:</strong> ${risk.encryption_date.split('T')[0]}<br>
                        <strong>🔒 Sensitivity:</strong> ${risk.sensitivity}<br>
                        <strong>⚠️ Vulnerable by:</strong> ${risk.breaking_year} (${risk.years_until_vulnerable} years)<br>
                        <strong>🚨 Immediate Action:</strong> ${risk.needs_immediate_action ? 'YES' : 'NO'}
                    </div>
                    
                    <div style="padding: 20px; background: rgba(${risk.risk_score > 70 ? '248, 113, 113' : risk.risk_score > 40 ? '251, 191, 36' : '52, 211, 153'}, 0.1); border-left: 4px solid ${riskColor}; border-radius: 12px;">
                        <strong style="color: ${riskColor};">💡 Recommendation:</strong><br>
                        <p style="margin-top: 10px; color: var(--text-primary);">${risk.recommendation}</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: var(--danger)">Error: ${error.message}</p>`;
    }
});

// Chat Assistant
document.getElementById('sendChat').addEventListener('click', sendMessage);
document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();

    if (!question) return;

    const messagesDiv = document.getElementById('chatMessages');

    messagesDiv.innerHTML += `
        <div class="chat-message user">
            <div class="message-content">
                <strong>You:</strong>
                <p>${question}</p>
            </div>
        </div>
    `;

    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    messagesDiv.innerHTML += `
        <div class="chat-message bot" id="typing">
            <div class="message-content">
                <strong>🤖 Assistant:</strong>
                <p><i class="fas fa-spinner fa-spin"></i> Thinking...</p>
            </div>
        </div>
    `;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        document.getElementById('typing').remove();

        if (data.success) {
            messagesDiv.innerHTML += `
                <div class="chat-message bot">
                    <div class="message-content">
                        <strong>🤖 QBits Assistant:</strong>
                        <p>${data.answer.replace(/\n/g, '<br>')}</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('typing').remove();
        messagesDiv.innerHTML += `
            <div class="chat-message bot">
                <div class="message-content">
                    <strong>🤖 Assistant:</strong>
                    <p style="color: var(--danger);">Sorry, I encountered an error. Please try again.</p>
                </div>
            </div>
        `;
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Dashboard
function loadDashboard() {
    const contentDiv = document.getElementById('dashboardContent');

    fetch('/api/security-dashboard')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const dashboard = data.dashboard;

                contentDiv.innerHTML = `
                    <div class="result-grid">
                        <div class="result-item">
                            <h4>Total Operations</h4>
                            <div class="value">${dashboard.total_operations}</div>
                            <small>Encryption operations monitored</small>
                        </div>
                        <div class="result-item">
                            <h4>Anomalies Detected</h4>
                            <div class="value" style="color: ${dashboard.anomalies_detected > 0 ? 'var(--danger)' : 'var(--success)'}">
                                ${dashboard.anomalies_detected}
                            </div>
                            <small>${dashboard.anomaly_rate.toFixed(1)}% anomaly rate</small>
                        </div>
                        <div class="result-item">
                            <h4>Threat Level</h4>
                            <div class="value" style="color: ${dashboard.threat_level === 'HIGH' ? 'var(--danger)' : 'var(--success)'}">
                                ${dashboard.threat_level}
                            </div>
                            <small>Overall security status</small>
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px; padding: 25px; background: var(--glass-bg); backdrop-filter: blur(10px); border: 1px solid var(--glass-border); border-radius: 16px;">
                        <h3 style="color: var(--primary); margin-bottom: 15px;">
                            <i class="fas fa-info-circle"></i> AI Security Monitoring
                        </h3>
                        <p style="color: var(--text-secondary); line-height: 1.8;">
                            Our AI-powered security monitoring system uses machine learning to detect anomalies in encryption operations.
                            It analyzes patterns like file size, encryption time, and operation timing to identify potential security threats.
                            <br><br>
                            All encryption operations are continuously monitored for unusual behavior patterns that could indicate
                            security issues or attacks.
                        </p>
                    </div>
                `;
            }
        })
        .catch(err => {
            contentDiv.innerHTML = '<p style="color: var(--danger)">Error loading dashboard</p>';
        });
}

// ==================== DECRYPT TAB ====================

let decryptSessionId = null;
let selectedDecryptFile = null;

document.addEventListener('DOMContentLoaded', () => {
    initializeDecryptTab();
});

function initializeDecryptTab() {
    const generateKeysBtn = document.getElementById('decryptGenerateKeys');
    const fileInput = document.getElementById('decryptFileInput');
    const fileNameDiv = document.getElementById('decryptFileName');
    const decryptBtn = document.getElementById('decryptBtn');

    if (!generateKeysBtn) return;  // tab not present

    // Step 1: Load the SAME session keys used during encryption
    generateKeysBtn.addEventListener('click', async () => {
        const keyStatusDiv = document.getElementById('decryptKeyStatus');

        // ✅ KEY FIX: Reuse the existing encryption session so the keys match
        if (sessionId) {
            decryptSessionId = sessionId;
            keyStatusDiv.style.display = '';
            keyStatusDiv.className = 'status-message success';
            keyStatusDiv.innerHTML = `✅ Encryption session keys loaded! Session: <code style="font-size:0.75rem;">${decryptSessionId.substring(0, 16)}…</code><br>
                <small style="opacity:0.8;">🔑 Using the same keys from your encryption session — decryption will work correctly.</small>`;
            generateKeysBtn.innerHTML = '<i class="fas fa-check"></i> Keys Loaded';
            generateKeysBtn.disabled = true;
            return;
        }

        // Fallback: no encryption session yet — generate new keys
        generateKeysBtn.disabled = true;
        generateKeysBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating keys...';
        keyStatusDiv.style.display = '';
        keyStatusDiv.className = 'status-message';
        keyStatusDiv.textContent = '🔑 No prior session found — generating new keys...';

        try {
            const response = await fetch('/api/generate-keys', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ algorithm: 'kyber768' })
            });
            const data = await response.json();

            if (data.success) {
                decryptSessionId = data.session_id;
                keyStatusDiv.style.display = '';
                keyStatusDiv.className = 'status-message success';
                keyStatusDiv.innerHTML = `✅ New keys generated. Session: <code style="font-size:0.75rem;">${decryptSessionId.substring(0, 16)}…</code><br>
                    <small style="opacity:0.8;">⚠️ These are NEW keys — only use to decrypt files encrypted in this same session.</small>`;
                generateKeysBtn.innerHTML = '<i class="fas fa-check"></i> Keys Loaded';
            } else {
                keyStatusDiv.style.display = '';
                keyStatusDiv.className = 'status-message error';
                keyStatusDiv.textContent = `❌ Key generation failed: ${data.error}`;
                generateKeysBtn.disabled = false;
                generateKeysBtn.innerHTML = '<i class="fas fa-key"></i> Generate / Load Keys';
            }
        } catch (err) {
            keyStatusDiv.style.display = '';
            keyStatusDiv.className = 'status-message error';
            keyStatusDiv.textContent = `❌ Error: ${err.message}`;
            generateKeysBtn.disabled = false;
            generateKeysBtn.innerHTML = '<i class="fas fa-key"></i> Generate / Load Keys';
        }
    });

    // Step 2: File picker (for .encrypted file)
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            selectedDecryptFile = fileInput.files[0];
            fileNameDiv.textContent = `📄 ${selectedDecryptFile.name}`;
            decryptBtn.disabled = false;
        }
    });

    // Key File import (Option B: load keys from a previous session)
    const keyFileInput = document.getElementById('keyFileInput');
    if (keyFileInput) {
        keyFileInput.addEventListener('change', async () => {
            if (!keyFileInput.files.length) return;

            const keyFile = keyFileInput.files[0];
            document.getElementById('keyFileName').textContent = keyFile.name;

            const importStatusDiv = document.getElementById('importKeyStatus');
            importStatusDiv.style.display = '';
            importStatusDiv.className = 'status-message';
            importStatusDiv.textContent = '🔑 Importing key file...';

            try {
                const formData = new FormData();
                formData.append('keyfile', keyFile);

                const response = await fetch('/api/import-keys', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    decryptSessionId = data.session_id;
                    importStatusDiv.style.display = '';
                    importStatusDiv.className = 'status-message success';
                    importStatusDiv.innerHTML = `✅ Key file loaded! Session: <code style="font-size:0.75rem;">${decryptSessionId.substring(0, 16)}…</code><br>
                        <small style="opacity:0.8;">🔓 You can now decrypt files encrypted with these keys.</small>`;

                    // Also update the main key status
                    const keyStatusDiv = document.getElementById('decryptKeyStatus');
                    keyStatusDiv.style.display = '';
                    keyStatusDiv.className = 'status-message success';
                    keyStatusDiv.textContent = '✅ Keys loaded from key file.';
                    generateKeysBtn.innerHTML = '<i class="fas fa-check"></i> Keys Loaded';
                    generateKeysBtn.disabled = true;
                } else {
                    importStatusDiv.style.display = '';
                    importStatusDiv.className = 'status-message error';
                    importStatusDiv.textContent = `❌ Import failed: ${data.error}`;
                }
            } catch (err) {
                importStatusDiv.style.display = '';
                importStatusDiv.className = 'status-message error';
                importStatusDiv.textContent = `❌ Error: ${err.message}`;
            }
        });
    }



    // Step 2: Decrypt click
    decryptBtn.addEventListener('click', async () => {
        if (!selectedDecryptFile) {
            alert('Please select a .encrypted file first.');
            return;
        }
        // Use decryptSessionId (which may be the shared encryption sessionId)
        const activeSession = decryptSessionId || sessionId;
        if (!activeSession) {
            alert('Please click "Generate / Load Keys" first (Step 1).');
            return;
        }
        decryptSessionId = activeSession;


        const decryptStatusDiv = document.getElementById('decryptStatus');
        decryptBtn.disabled = true;
        decryptBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Decrypting...';
        decryptStatusDiv.style.display = '';
        decryptStatusDiv.className = 'status-message';
        decryptStatusDiv.textContent = '🔓 Decrypting your file...';

        try {
            const formData = new FormData();
            formData.append('session_id', decryptSessionId);
            formData.append('file', selectedDecryptFile);

            const response = await fetch('/api/decrypt', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                // Try to parse JSON error
                let errMsg = `Server error ${response.status}`;
                try {
                    const errData = await response.json();
                    errMsg = errData.error || errMsg;
                } catch (_) { }
                throw new Error(errMsg);
            }

            // Get filename from Content-Disposition header if available
            const disposition = response.headers.get('Content-Disposition');
            let downloadName = 'decrypted_file';
            if (disposition) {
                const match = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (match && match[1]) {
                    downloadName = match[1].replace(/['"]/g, '');
                }
            } else {
                // Fall back to stripping .encrypted from original name
                downloadName = selectedDecryptFile.name.replace(/\.encrypted$/i, '');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = downloadName;
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                URL.revokeObjectURL(url);
                a.remove();
            }, 1000);

            decryptStatusDiv.style.display = '';
            decryptStatusDiv.className = 'status-message success';
            decryptStatusDiv.innerHTML = `✅ File decrypted and downloaded as <strong>${downloadName}</strong>`;
        } catch (err) {
            decryptStatusDiv.style.display = '';
            decryptStatusDiv.className = 'status-message error';
            decryptStatusDiv.textContent = `❌ Decryption failed: ${err.message}`;
        } finally {
            decryptBtn.disabled = false;
            decryptBtn.innerHTML = '<i class="fas fa-unlock"></i> Decrypt File';
        }
    });
}

