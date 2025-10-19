"""
Integration tests for account routes and API.
"""

import json


def test_accounts_page_loads(client):
    """Test that accounts page loads successfully."""
    response = client.get('/accounts')
    assert response.status_code == 200
    assert b'Bank Accounts' in response.data


def test_get_accounts_empty(client):
    """Test getting accounts when none exist."""
    response = client.get('/api/accounts')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['accounts'] == []
    assert data['count'] == 0


def test_create_account_success(client):
    """Test creating an account successfully."""
    response = client.post('/api/accounts',
                          json={
                              'name': 'Test Checking',
                              'type': 'checking',
                              'institution': 'Test Bank'
                          })
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'account_id' in data
    assert data['account_id'] > 0


def test_create_account_missing_name(client):
    """Test creating account without name."""
    response = client.post('/api/accounts',
                          json={
                              'type': 'checking'
                          })
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'name' in data['error'].lower()


def test_create_account_missing_type(client):
    """Test creating account without type."""
    response = client.post('/api/accounts',
                          json={
                              'name': 'Test Account'
                          })
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'type' in data['error'].lower()


def test_create_account_invalid_type(client):
    """Test creating account with invalid type."""
    response = client.post('/api/accounts',
                          json={
                              'name': 'Test Account',
                              'type': 'invalid_type'
                          })
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False


def test_create_and_get_account(client):
    """Test creating and retrieving an account."""
    # Create account
    create_response = client.post('/api/accounts',
                                 json={
                                     'name': 'Test Account',
                                     'type': 'savings',
                                     'institution': 'My Bank'
                                 })
    
    create_data = json.loads(create_response.data)
    account_id = create_data['account_id']
    
    # Get specific account
    get_response = client.get(f'/api/accounts/{account_id}')
    assert get_response.status_code == 200
    
    get_data = json.loads(get_response.data)
    assert get_data['success'] is True
    assert get_data['account']['id'] == account_id
    assert get_data['account']['name'] == 'Test Account'
    assert get_data['account']['type'] == 'savings'
    assert get_data['account']['institution'] == 'My Bank'


def test_get_account_not_found(client):
    """Test getting non-existent account."""
    response = client.get('/api/accounts/99999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False


def test_get_all_accounts(client):
    """Test getting all accounts."""
    # Create multiple accounts
    client.post('/api/accounts',
               json={'name': 'Account 1', 'type': 'checking'})
    client.post('/api/accounts',
               json={'name': 'Account 2', 'type': 'savings'})
    client.post('/api/accounts',
               json={'name': 'Account 3', 'type': 'credit'})
    
    # Get all
    response = client.get('/api/accounts')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['count'] == 3
    assert len(data['accounts']) == 3


def test_update_account(client):
    """Test updating an account."""
    # Create account
    create_response = client.post('/api/accounts',
                                 json={'name': 'Old Name', 'type': 'checking'})
    account_id = json.loads(create_response.data)['account_id']
    
    # Update account
    update_response = client.put(f'/api/accounts/{account_id}',
                                json={'name': 'New Name'})
    
    assert update_response.status_code == 200
    
    update_data = json.loads(update_response.data)
    assert update_data['success'] is True
    
    # Verify update
    get_response = client.get(f'/api/accounts/{account_id}')
    get_data = json.loads(get_response.data)
    assert get_data['account']['name'] == 'New Name'


def test_update_account_not_found(client):
    """Test updating non-existent account."""
    response = client.put('/api/accounts/99999',
                         json={'name': 'New Name'})
    
    assert response.status_code == 404


def test_delete_account(client):
    """Test deleting an account."""
    # Create account
    create_response = client.post('/api/accounts',
                                 json={'name': 'To Delete', 'type': 'checking'})
    account_id = json.loads(create_response.data)['account_id']
    
    # Delete account
    delete_response = client.delete(f'/api/accounts/{account_id}')
    
    assert delete_response.status_code == 200
    
    delete_data = json.loads(delete_response.data)
    assert delete_data['success'] is True
    
    # Verify deleted
    get_response = client.get(f'/api/accounts/{account_id}')
    assert get_response.status_code == 404


def test_delete_account_not_found(client):
    """Test deleting non-existent account."""
    response = client.delete('/api/accounts/99999')
    
    assert response.status_code == 404

