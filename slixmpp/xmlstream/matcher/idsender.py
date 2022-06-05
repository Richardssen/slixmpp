# -*- coding: utf-8 -*-
"""
    slixmpp.xmlstream.matcher.id
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Part of Slixmpp: The Slick XMPP Library

    :copyright: (c) 2011 Nathanael C. Fritz
    :license: MIT, see LICENSE for more details
"""

from slixmpp.xmlstream.matcher.base import MatcherBase


class MatchIDSender(MatcherBase):

    """
    The IDSender matcher selects stanzas that have the same stanza 'id'
    interface value as the desired ID, and that the 'from' value is one
    of a set of approved entities that can respond to a request.
    """

    def match(self, xml):
        """Compare the given stanza's ``'id'`` attribute to the stored
        ``id`` value, and verify the sender's JID.

        :param xml: The :class:`~slixmpp.xmlstream.stanzabase.ElementBase`
                    stanza to compare against.
        """

        selfjid = self._criteria['self']
        peerjid = self._criteria['peer']

        allowed = {
            '': True,
            selfjid.bare: True,
            selfjid.host: True,
            peerjid.full: True,
            peerjid.bare: True,
            peerjid.host: True,
        }

        _from = xml['from']

        try:
            return xml['id'] == self._criteria['id'] and allowed[_from]
        except KeyError:
            return False
