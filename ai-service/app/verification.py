from typing import Dict, Any


class EvidenceVerifier:
    @staticmethod
    def verify_claim(claim: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        numeric_claim = evidence.get('numeric_claim')
        if numeric_claim is None:
            return {'status': 'UNSUPPORTED', 'reason': 'No numeric claim provided'}

        current_value = evidence.get('current_value')
        baseline_value = evidence.get('baseline_value')
        if current_value is not None and baseline_value is not None:
            calc = ((current_value - baseline_value) / baseline_value) * 100
            within_tolerance = abs(calc - numeric_claim) <= 2.0
            return {
                'status': 'SUPPORTED' if within_tolerance else 'UNSUPPORTED',
                'calculated_change': round(calc, 2),
                'expected_value': numeric_claim,
                'tolerance': 2.0,
                'claim': claim
            }

        return {
            'status': 'SUPPORTED' if claim else 'UNSUPPORTED',
            'claim': claim
        }
