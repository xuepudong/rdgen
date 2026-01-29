#!/bin/bash

# Script to test macOS certificate locally

set -e

CERTS_DIR="certs"
P12_FILE="$CERTS_DIR/certificate.p12"
BASE64_FILE="$CERTS_DIR/certificate_base64.txt"

echo "=== Testing Local macOS Certificate ==="
echo ""

# Check if files exist
if [ ! -f "$P12_FILE" ]; then
    echo "❌ ERROR: Certificate file not found: $P12_FILE"
    exit 1
fi

if [ ! -f "$BASE64_FILE" ]; then
    echo "❌ ERROR: Base64 file not found: $BASE64_FILE"
    exit 1
fi

echo "✅ Certificate files found"
echo "   P12 file: $P12_FILE"
echo "   Base64 file: $BASE64_FILE"
echo ""

# Check file sizes
P12_SIZE=$(stat -f%z "$P12_FILE")
BASE64_CONTENT=$(cat "$BASE64_FILE")
BASE64_LENGTH=${#BASE64_CONTENT}

echo "=== File Information ==="
echo "   P12 size: $P12_SIZE bytes"
echo "   Base64 length: $BASE64_LENGTH characters"
echo ""

# Verify base64 encoding
echo "=== Verifying Base64 Encoding ==="
BASE64_FROM_P12=$(base64 -i "$P12_FILE" | tr -d '\n')
if [ "$BASE64_FROM_P12" = "$BASE64_CONTENT" ]; then
    echo "✅ Base64 file matches P12 file"
else
    echo "⚠️  WARNING: Base64 file does not match P12 file"
    echo "   This might cause issues with GitHub Secrets"
    echo "   Regenerate with: base64 -i $P12_FILE | tr -d '\n' > $BASE64_FILE"
fi
echo ""

# Test password (if provided)
echo "=== Testing Certificate Password ==="
read -sp "Enter the P12 password (or press Enter to skip): " P12_PASSWORD
echo ""

if [ -n "$P12_PASSWORD" ]; then
    # Check if rcodesign is installed
    if command -v rcodesign &> /dev/null; then
        echo "Testing with rcodesign..."
        if rcodesign extract --p12-file "$P12_FILE" --p12-password "$P12_PASSWORD" > /dev/null 2>&1; then
            echo "✅ Password is CORRECT! Certificate can be decrypted."
            echo ""
            echo "=== Certificate Details ==="
            rcodesign print-signing-certificate --p12-file "$P12_FILE" --p12-password "$P12_PASSWORD" || true
        else
            echo "❌ ERROR: Password is INCORRECT or certificate is invalid!"
            exit 1
        fi
    elif command -v openssl &> /dev/null; then
        echo "Testing with openssl..."
        if openssl pkcs12 -in "$P12_FILE" -passin pass:"$P12_PASSWORD" -noout > /dev/null 2>&1; then
            echo "✅ Password is CORRECT! Certificate can be decrypted."
            echo ""
            echo "=== Certificate Details ==="
            openssl pkcs12 -in "$P12_FILE" -passin pass:"$P12_PASSWORD" -nokeys -info 2>/dev/null || true
        else
            echo "❌ ERROR: Password is INCORRECT or certificate is invalid!"
            exit 1
        fi
    else
        echo "⚠️  WARNING: Neither rcodesign nor openssl found"
        echo "   Cannot test password validity"
        echo "   Install rcodesign: https://github.com/indygreg/apple-platform-rs"
    fi
else
    echo "ℹ️  Password test skipped"
fi

echo ""
echo "=== GitHub Secrets Setup ==="
echo "To upload to GitHub Secrets:"
echo "1. Go to: https://github.com/YOUR_USERNAME/rdgen/settings/secrets/actions"
echo "2. Add/Update secret: MACOS_P12_BASE64"
echo "   Value: $(head -c 50 "$BASE64_FILE")... (${BASE64_LENGTH} chars total)"
echo "3. Add/Update secret: MACOS_P12_PASSWORD"
echo "   Value: Your certificate password"
echo ""
echo "✅ Local certificate verification complete!"
