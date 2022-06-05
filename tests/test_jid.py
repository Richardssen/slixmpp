# -*- encoding: utf8 -*-
from __future__ import unicode_literals
import unittest
from slixmpp.test import SlixTest
from slixmpp import JID, InvalidJID
from slixmpp.jid import nodeprep


class TestJIDClass(SlixTest):

    """Verify that the JID class can parse and manipulate JIDs."""

    def testJIDFromFull(self):
        """Test using JID of the form 'user@server/resource/with/slashes'."""
        self.check_jid(JID('user@someserver/some/resource'),
                       'user',
                       'someserver',
                       'some/resource',
                       'user@someserver',
                       'user@someserver/some/resource',
                       'user@someserver/some/resource')

    def testJIDchange(self):
        """Test changing JID of the form 'user@server/resource/with/slashes'"""
        j = JID('user1@someserver1/some1/resource1')
        j.user = 'user'
        j.domain = 'someserver'
        j.resource = 'some/resource'
        self.check_jid(j,
                       'user',
                       'someserver',
                       'some/resource',
                       'user@someserver',
                       'user@someserver/some/resource',
                       'user@someserver/some/resource')

    def testJIDaliases(self):
        """Test changing JID using aliases for domain."""
        j = JID('user@someserver/resource')
        j.server = 'anotherserver'
        self.check_jid(j, domain='anotherserver')
        j.host = 'yetanother'
        self.check_jid(j, domain='yetanother')

    def testJIDSetFullWithUser(self):
        """Test setting the full JID with a user portion."""
        j = JID('user@domain/resource')
        j.full = 'otheruser@otherdomain/otherresource'
        self.check_jid(j,
                       'otheruser',
                       'otherdomain',
                       'otherresource',
                       'otheruser@otherdomain',
                       'otheruser@otherdomain/otherresource',
                       'otheruser@otherdomain/otherresource')

    def testJIDFullNoUserWithResource(self):
        """
        Test setting the full JID without a user
        portion and with a resource.
        """
        j = JID('user@domain/resource')
        j.full = 'otherdomain/otherresource'
        self.check_jid(j,
                       '',
                       'otherdomain',
                       'otherresource',
                       'otherdomain',
                       'otherdomain/otherresource',
                       'otherdomain/otherresource')

    def testJIDFullNoUserNoResource(self):
        """
        Test setting the full JID without a user
        portion and without a resource.
        """
        j = JID('user@domain/resource')
        j.full = 'otherdomain'
        self.check_jid(j,
                       '',
                       'otherdomain',
                       '',
                       'otherdomain',
                       'otherdomain',
                       'otherdomain')

    def testJIDBareUser(self):
        """Test setting the bare JID with a user."""
        j = JID('user@domain/resource')
        j.bare = 'otheruser@otherdomain'
        self.check_jid(j,
                       'otheruser',
                       'otherdomain',
                       'resource',
                       'otheruser@otherdomain',
                       'otheruser@otherdomain/resource',
                       'otheruser@otherdomain/resource')

    def testJIDBareNoUser(self):
        """Test setting the bare JID without a user."""
        j = JID('user@domain/resource')
        j.bare = 'otherdomain'
        self.check_jid(j,
                       '',
                       'otherdomain',
                       'resource',
                       'otherdomain',
                       'otherdomain/resource',
                       'otherdomain/resource')

    def testJIDNoResource(self):
        """Test using JID of the form 'user@domain'."""
        self.check_jid(JID('user@someserver'),
                       'user',
                       'someserver',
                       '',
                       'user@someserver',
                       'user@someserver',
                       'user@someserver')

    def testJIDNoUser(self):
        """Test JID of the form 'component.domain.tld'."""
        self.check_jid(JID('component.someserver'),
                       '',
                       'component.someserver',
                       '',
                       'component.someserver',
                       'component.someserver',
                       'component.someserver')

    def testJIDEquality(self):
        """Test that JIDs with the same content are equal."""
        jid1 = JID('user@domain/resource')
        jid2 = JID('user@domain/resource')
        self.assertTrue(jid1 == jid2, "Same JIDs are not considered equal")
        self.assertFalse(jid1 != jid2, "Same JIDs are considered not equal")

    def testJIDInequality(self):
        jid1 = JID('user@domain/resource')
        jid2 = JID('otheruser@domain/resource')
        self.assertFalse(jid1 == jid2, "Different JIDs are considered equal")
        self.assertTrue(jid1 != jid2, "Different JIDs are considered equal")

    def testZeroLengthDomain(self):
        jid1 = JID('')
        jid2 = JID()
        self.assertTrue(jid1 == jid2, "Empty JIDs are not considered equal")
        self.assertTrue(jid1.domain == '', "Empty JID’s domain part not empty")
        self.assertTrue(jid1.full == '', "Empty JID’s full part not empty")

        self.assertRaises(InvalidJID, JID, 'user@')
        self.assertRaises(InvalidJID, JID, '/resource')
        self.assertRaises(InvalidJID, JID, 'user@/resource')

    def testZeroLengthLocalPart(self):
        self.assertRaises(InvalidJID, JID, '@test.com')
        self.assertRaises(InvalidJID, JID, '@test.com/resource')

    def testZeroLengthNodeDomain(self):
        self.assertRaises(InvalidJID, JID, '@/test.com')

    def testZeroLengthResource(self):
        self.assertRaises(InvalidJID, JID, 'test.com/')
        self.assertRaises(InvalidJID, JID, 'user@test.com/')

    def test1023LengthDomain(self):
        jid = JID(f"user@{'a.' * 509 + 'a.com'}/resource")

    def test1023LengthLocalPart(self):
        jid = JID(f"{'a' * 1023}@test.com")

    def test1023LengthResource(self):
        jid = JID(f"test.com/{'r' * 1023}")

    def test1024LengthDomain(self):
        domain = ('a.' * 509) + 'aa.com'
        self.assertRaises(InvalidJID, JID, f'user@{domain}/resource')
        self.assertRaises(InvalidJID, JID, f'user@{domain}')
        self.assertRaises(InvalidJID, JID, f'{domain}/resource')
        self.assertRaises(InvalidJID, JID, domain)

    def test1024LengthLocalPart(self):
        local = 'a' * 1024
        self.assertRaises(InvalidJID, JID, f'{local}@test.com')
        self.assertRaises(InvalidJID, JID, f'{local}@test.com/resource')

    def test1024LengthResource(self):
        resource = 'r' * 1024
        self.assertRaises(InvalidJID, JID, f'test.com/{resource}')
        self.assertRaises(InvalidJID, JID, f'user@test.com/{resource}')

    def testTooLongDomainLabel(self):
        self.assertRaises(InvalidJID, JID, f"user@{'a' * 64 + '.com'}/resource")

    def testDomainEmptyLabel(self):
        self.assertRaises(InvalidJID, JID, 'user@aaa..bbb.com/resource')

    def testDomainIPv4(self):
        domain = '127.0.0.1'

        jid1 = JID(f'{domain}')
        jid2 = JID(f'user@{domain}')
        jid3 = JID(f'{domain}/resource')
        jid4 = JID(f'user@{domain}/resource')

    def testDomainIPv6(self):
        domain = '[::1]'

        jid1 = JID(f'{domain}')
        jid2 = JID(f'user@{domain}')
        jid3 = JID(f'{domain}/resource')
        jid4 = JID(f'user@{domain}/resource')

    def testDomainInvalidIPv6NoBrackets(self):
        domain = '::1'

        self.assertRaises(InvalidJID, JID, f'{domain}')
        self.assertRaises(InvalidJID, JID, f'user@{domain}')
        self.assertRaises(InvalidJID, JID, f'{domain}/resource')
        self.assertRaises(InvalidJID, JID, f'user@{domain}/resource')

    def testDomainInvalidIPv6MissingBracket(self):
        domain = '[::1'

        self.assertRaises(InvalidJID, JID, f'{domain}')
        self.assertRaises(InvalidJID, JID, f'user@{domain}')
        self.assertRaises(InvalidJID, JID, f'{domain}/resource')
        self.assertRaises(InvalidJID, JID, f'user@{domain}/resource')

    def testDomainInvalidIPv6WrongBracket(self):
        domain = '[::]1]'

        self.assertRaises(InvalidJID, JID, f'{domain}')
        self.assertRaises(InvalidJID, JID, f'user@{domain}')
        self.assertRaises(InvalidJID, JID, f'{domain}/resource')
        self.assertRaises(InvalidJID, JID, f'user@{domain}/resource')

    def testDomainWithPort(self):
        domain = 'example.com:5555'

        self.assertRaises(InvalidJID, JID, f'{domain}')
        self.assertRaises(InvalidJID, JID, f'user@{domain}')
        self.assertRaises(InvalidJID, JID, f'{domain}/resource')
        self.assertRaises(InvalidJID, JID, f'user@{domain}/resource')

    def testDomainWithTrailingDot(self):
        jid = JID('user@example.com./resource')

        self.assertEqual(jid.domain, 'example.com')

    def testDomainWithDashes(self):
        self.assertRaises(InvalidJID, JID, 'user@example.com-/resource')

        self.assertRaises(InvalidJID, JID, 'user@-example.com/resource')

    def testACEDomain(self):
        jid = JID('user@xn--bcher-kva.ch/resource')

        self.assertEqual(jid.domain.encode('utf-8'), b'b\xc3\xbccher.ch')

    def testJIDUnescape(self):
        jid = JID('here\\27s_a_wild_\\26_\\2fcr%zy\\2f_\\40ddress\\20for\\3a\\3cwv\\3e(\\22IMPS\\22)\\5c@example.com')
        ujid = jid.unescape()
        self.assertEqual(ujid.local, 'here\'s_a_wild_&_/cr%zy/_@ddress for:<wv>("imps")\\')

        jid = JID('blah\\5cfoo\\5c20bar@example.com')
        ujid = jid.unescape()
        self.assertEqual(ujid.local, 'blah\\foo\\20bar')

    def testStartOrEndWithEscapedSpaces(self):
        self.assertRaises(InvalidJID, JID, ' foo@example.com')

        self.assertRaises(InvalidJID, JID, 'bar @example.com')

        # Need more input for these cases. A JID starting with \20 *is* valid
        # according to RFC 6122, but is not according to XEP-0106.
        #self.assertRaises(InvalidJID, JID, '%s@example.com' % '\\20foo2')
        #self.assertRaises(InvalidJID, JID, '%s@example.com' % 'bar2\\20')

    def testNodePrepIdemptotent(self):
        node = 'ᴹᴵᴷᴬᴱᴸ'
        self.assertEqual(nodeprep(node), nodeprep(nodeprep(node)))


suite = unittest.TestLoader().loadTestsFromTestCase(TestJIDClass)
