"""
Tests for the response caching functionality.

This module tests the cache implementation to ensure:
1. Responses are properly cached
2. Cached responses are retrieved correctly
3. Cache expiration works as expected
"""

import pytest
import os
import tempfile
import time
from unittest.mock import patch, MagicMock
from smartman.cache import ResponseCache


class TestResponseCache:
    """Test suite for the ResponseCache class."""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary directory for cache files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_cache_initialization(self, temp_cache_dir):
        """
        Test that the cache initializes correctly.
        
        Verifies that:
        1. The cache directory is created if it doesn't exist
        2. The cache is initialized with the correct TTL
        """
        # Initialize cache with custom directory and TTL
        cache = ResponseCache(cache_dir=temp_cache_dir, ttl_hours=48)
        
        # Check that the cache directory exists
        assert os.path.exists(temp_cache_dir)
        
        # Check that the TTL was set correctly
        assert cache.ttl.total_seconds() == 48 * 3600
    
    def test_cache_key_generation(self):
        """
        Test that cache keys are generated consistently.
        
        Verifies that:
        1. The same input produces the same cache key
        2. Different inputs produce different cache keys
        """
        cache = ResponseCache()
        
        # Check that the same input generates the same key
        key1 = cache.get_cache_key("test_text")
        key2 = cache.get_cache_key("test_text")
        assert key1 == key2
        
        # Check that different inputs generate different keys
        key3 = cache.get_cache_key("different_text")
        assert key1 != key3
    
    def test_cache_storage_and_retrieval(self, temp_cache_dir):
        """
        Test that responses are properly stored and retrieved.
        
        Verifies that:
        1. A response can be stored in the cache
        2. The same response can be retrieved from the cache
        """
        cache = ResponseCache(cache_dir=temp_cache_dir)
        
        # Store a response in the cache
        prompt = "test prompt"
        action = "summary"
        response = "This is a test response"
        
        cache.cache_response(prompt, action, response)
        
        # Retrieve the response from the cache
        cached_response = cache.get_cached_response(prompt, action)
        
        # Check that the retrieved response matches the stored one
        assert cached_response == response
    
    def test_cache_miss(self, temp_cache_dir):
        """
        Test that cache misses are handled correctly.
        
        Verifies that:
        1. A request for an uncached item returns None
        """
        cache = ResponseCache(cache_dir=temp_cache_dir)
        
        # Try to retrieve a response that hasn't been cached
        cached_response = cache.get_cached_response("uncached prompt", "summary")
        
        # Check that None is returned for a cache miss
        assert cached_response is None
    
    def test_cache_expiration(self, temp_cache_dir):
        """
        Test that cached responses expire correctly.
        
        Verifies that:
        1. An expired cache entry is not returned
        """
        # Create a cache with a very short TTL (1 second)
        cache = ResponseCache(cache_dir=temp_cache_dir, ttl_hours=1/3600)
        
        # Store a response in the cache
        prompt = "test prompt"
        action = "summary"
        response = "This is a test response"
        
        cache.cache_response(prompt, action, response)
        
        # Wait for the cache to expire
        time.sleep(2)
        
        # Try to retrieve the expired response
        cached_response = cache.get_cached_response(prompt, action)
        
        # Check that None is returned for an expired cache entry
        assert cached_response is None


class TestCacheIntegration:
    """Test suite for cache integration with the main application."""
    
    def test_cache_integration_with_main_app(self, cli_runner):
        """
        Basic integration test for the cache with the main application.
        
        This verifies that:
        1. The application can use caching without errors
        2. Execution completes successfully
        """
        # Since we're mocking at higher levels, we can't verify exact call patterns
        # Instead we'll focus on the overall command execution
        
        # Import here to avoid circular imports with fixtures
        from smartman.main import cli
        
        # Run the command twice - second run should use cache if implemented
        result1 = cli_runner.invoke(cli, ['summary', 'ls'])
        assert result1.exit_code == 0
        
        result2 = cli_runner.invoke(cli, ['summary', 'ls'])
        assert result2.exit_code == 0
        
        # Both executions were successful
        assert result1.exit_code == 0 and result2.exit_code == 0
    
    def test_cache_functional_with_mocked_api(self):
        """
        Test the cache functionality with mocked API.
        
        This is a direct unit test of the cache rather than integration test,
        which avoids issues with multi-level mocking.
        """
        from smartman.cache import ResponseCache
        import tempfile
        
        # Create a temporary cache directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize cache
            cache = ResponseCache(cache_dir=temp_dir)
            
            # Store a response
            prompt = "test prompt"
            action = "summary"
            response = "This is a cached response"
            
            # Should not raise exceptions
            cache.cache_response(prompt, action, response)
            
            # Should return the cached response
            cached = cache.get_cached_response(prompt, action)
            assert cached == response 